import cv2
import numpy as np
from tensorflow.keras import backend as K

from ..models import load_model
from ..config import Config

def read_img(filepath):
    """
        Reads an image from the destination directory and convert to thresholded image np array
    """
    img = cv2.imread(filepath)
    original_image = img.copy()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    height, width, colours = img.shape

    if width > 1000:

        new_width = 1000
        aspect_ratio = width / height
        new_height = int(new_width / aspect_ratio)

        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    thresh_img = threshold_image(img)

    return original_image, thresh_img

def threshold_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)

    return thresh

def segment_line(image):
    """
    Segments images by lines of sentences
    """
    # dilate image
    kernel = np.ones((3, 85), np.uint8)
    dilated = cv2.dilate(image, kernel, iterations=1)

    # find contours of lines
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours_lines = sorted(contours, key=lambda cnt: cv2.boundingRect(cnt)[1]) # sort according to y

    return sorted_contours_lines

def segment_words(image):
    """
    Segments images by words according to the segmented lines
    """
    words = []
    lines = segment_line(image)

    # dilate the image
    kernel = np.ones((3, 14), np.uint8)
    dilated = cv2.dilate(image, kernel, iterations=1)

    for line in lines:

        # roi of each line
        x, y, width, height = cv2.boundingRect(line)
        roi_line = dilated[y:y+height, x:x+width]

        # draw contours on each word
        contours, hierarchy = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contours_words = sorted(contours, key=lambda cnt: cv2.boundingRect(cnt)[0]) # sort according to x

        for word_contour in sorted_contours_words:

            if cv2.contourArea(word_contour) < 100:
                continue

            x2, y2, width2, height2 = cv2.boundingRect(word_contour)
            words.append([x+x2, y+y2, x+x2+width2, y+y2+height2])

    return words

def process_segmented_image(segmented):
    """
    Convert word image to shape (32, 128, 1) & normalize
    """

    img = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
    width, height = img.shape

    # aspect ratio calculation
    new_width = 32
    new_height = int(height * (new_width / width))
    img = cv2.resize(img, (new_height, new_width))
    width, height = img.shape

    img = img.astype("float32")

    # converts each to (32, 128, 1)
    if width < 32:
        add_zeros = np.full((32 - width, height), 255)
        img = np.concatenate((img, add_zeros))
        width, height = img.shape

    if height < 128:
        add_zeros = np.full((width, 128 - height), 255)
        img = np.concatenate((img, add_zeros), axis=1)
        width, height = img.shape

    if height > 128 or width > 32:
        dim = (128, 32)
        img = cv2.resize(img, dim)

    img = cv2.subtract(255, img)
    img = np.expand_dims(img, axis=2)

    # normalize the image
    img = img / 255

    return img

def predict_img(model, segmented):
    """
        Predict the text contained in a segmented image and return single word predicted
    """
    img = np.asarray([process_segmented_image(segmented)])
    prediction = model.predict(img, verbose=0)

    decoded = K.ctc_decode(
        prediction,
        input_length=np.ones(prediction.shape[0]) * prediction.shape[1],
        greedy=True
    )[0][0]

    out = K.get_value(decoded)

    for i, x in enumerate(out):
        text = ""
        for p in x:
            if int(p) != -1:
                text += Config.CHAR_LIST[int(p)]

    return text

def convert_image_to_text(filepath):
    """
        converting entire image to sentences and return them to the client
    """
    model = load_model()
    original_image, thresh_image = read_img(filepath)
    words = segment_words(thresh_image)
    whole_text = []

    for word in words:
        segmented = original_image[word[1]:word[3], word[0]:word[2]]
        predicted_word = predict_img(model, segmented)
        whole_text.append(predicted_word)

    whole_text = " ".join(whole_text)

    return whole_text
