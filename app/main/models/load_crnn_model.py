from tensorflow.keras.layers import (
    Dense,
    LSTM,
    Reshape,
    BatchNormalization,
    Input,
    Conv2D,
    MaxPooling2D,
    Lambda,
    Bidirectional
)
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
import tensorflow as tf
from ..config import Config

def create_crnn_model():
    inputs = Input(shape=(32, 128, 1))

    conv_1 = Conv2D(filters=64, kernel_size=(3, 3), activation="relu", padding="same")(inputs)
    pool_1 = MaxPooling2D(pool_size=2, strides=2)(conv_1)

    conv_2 = Conv2D(filters=128, kernel_size=(3, 3), activation="relu", padding="same")(pool_1)
    pool_2 = MaxPooling2D(pool_size=2, strides=2)(conv_2)

    conv_3 = Conv2D(filters=256, kernel_size=(3, 3), activation="relu", padding="same")(pool_2)
    conv_4 = Conv2D(filters=256, kernel_size=(3, 3), activation="relu", padding="same")(conv_3)
    pool_4 = MaxPooling2D(pool_size=(2, 1))(conv_4)

    conv_5 = Conv2D(filters=512, kernel_size=(3, 3), activation="relu", padding="same")(pool_4)
    batch_norm_5 = BatchNormalization()(conv_5)

    conv_6 = Conv2D(filters=512, kernel_size=(3, 3), activation="relu", padding="same")(batch_norm_5)
    batch_norm_6 = BatchNormalization()(conv_6)
    pool_6 = MaxPooling2D(pool_size=(2, 1))(batch_norm_6)

    conv_7 = Conv2D(filters=512, kernel_size=(2, 2), activation="relu")(pool_6)
    squeezed = Lambda(lambda x: K.squeeze(x, 1))(conv_7)

    blstm_1 = Bidirectional(LSTM(256, return_sequences=True, dropout=0.2))(squeezed)
    blstm_2 = Bidirectional(LSTM(256, return_sequences=True, dropout=0.2))(blstm_1)
    outputs = Dense(Config.CHAR_LENGTH + 1, activation="softmax")(blstm_2) # 79 char list

    act_model = Model(inputs, outputs)

    return act_model

def ctc_lambda_function(args):
    y_pred, labels, input_length, label_length = args

    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


def load_model():

    model = create_crnn_model()
    model.compile(
        loss={'ctc': lambda y_true, y_pred: y_pred},
        optimizer=tf.keras.optimizers.SGD(),
        metrics=["accuracy"]
    )

    model.load_weights(f"app\\main\\models\\trained_model.h5")

    return model
