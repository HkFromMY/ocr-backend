from flask_restx import Namespace, Resource

from ..utils import SuccessResponse, ErrorResponse, ValidationError
from ..constants import HttpCode
from ..validations import convert_upload_parser
from ..services import convert_image_to_text
from ..config import Config
from ..utils import delete_file

convert = Namespace(
    name="Convert Image",
    description="Convert image given to text with the tensorflow model"
)

@convert.route("/convert")
class Convert(Resource):
    """
    Handles convert request
    """

    def post(self):
        # validation for data
        parser = convert_upload_parser()
        fields = parser.parse_args()

        # file content (image uploaded)
        image = fields.get("images")

        # if any file type other than image files then reject them
        if not image.mimetype.startswith("image"):
            raise ValidationError(
                message="Invalid file type",
                errors={ 'images': 'Invalid file type' }
            )

        filename = image.filename
        file_dst = f"{Config.UPLOAD_DIR}\\{filename}"

        # save the image to destination directory and close the file stream
        image.save(file_dst)
        image.close()

        # convert image to text with service function
        whole_text = convert_image_to_text(file_dst)

        # delete the file
        delete_file(file_dst)

        # return response
        return SuccessResponse(
            message="Successful converting the image to text",
            data={ "text": whole_text }
        ).to_dict()
