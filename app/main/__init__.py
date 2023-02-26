from flask import Flask
from flask_cors import CORS

def create_app():

    app = Flask(__name__)

    # setting up CORS
    CORS(app)

    # setting upload directory
    app.config['UPLOAD_FOLDER'] = "app\\uploads\\user\\images"

    return app
