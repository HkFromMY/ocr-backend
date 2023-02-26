from flask_restx import reqparse
from werkzeug.datastructures import FileStorage

def convert_upload_parser():
    parser = reqparse.RequestParser(bundle_errors=True) # make all the errors returned to the client at once
    parser.add_argument("images", type=FileStorage, location="files", required=True)

    return parser
