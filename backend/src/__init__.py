from typing import Tuple
from flask import Flask
from flask_pymongo import PyMongo
import os
from pathlib import Path
from backend.constants import FLASK_ENV, SECRET, SECRET_KEY, FLASK_ENV_TEST, DIR_TESTS, DIR_SRC


def create_app(config_filename: str) -> Tuple[Flask, PyMongo]:
    # Create Flask app
    flask_app = Flask(__name__)

    # Set the Flask app configuration based on the environment
    if os.getenv(FLASK_ENV) == FLASK_ENV_TEST:
        config_path = Path(__file__).resolve().parent.parent / DIR_TESTS / config_filename
    else:
        config_path = Path(__file__).resolve().parent.parent / DIR_SRC / config_filename

    flask_app.config.from_pyfile(config_path)

    # Configure MongoDB connection
    flask_app.config[SECRET_KEY] = SECRET
    mongo = PyMongo(flask_app)

    # Register blueprints or perform any additional setup

    return flask_app, mongo
