import logging
import os
from datetime import datetime, timezone, timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, set_access_cookies, get_jwt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
if app.config["ENV"] == "production":
    app.config.from_object("timebank.utils.config.ProductionConfig")
else:
    app.config.from_object("timebank.utils.config.DevelopmentConfig")

db = SQLAlchemy(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
jwt = JWTManager(app)


@app.before_first_request
def before_first_request():
    log_level = logging.DEBUG

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    app.logger.setLevel(log_level)
    default_formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s", datefmt='%y %b %d - %H:%M:%S')
    handler.setFormatter(default_formatter)


@app.after_request
def add_header(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add('X-Content-Type-Options', 'nosniff')

    if response.content_type == '':
        response.content_type = 'application/json'

    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


import timebank.models
import timebank.routes
import timebank.utils
