"""
    UFind-API.__init__.py

    This is the application level module. This file registers all the resources
    defined in the submodules.
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, blueprints
from flask_jwt import JWT
from flask_bcrypt import Bcrypt
from peewee import SqliteDatabase

import config
from app.auth import cb_authenticate, cb_identity

app = Flask(__name__)

db = SqliteDatabase(config.DATABASE_URI)
jwt = JWT(app, cb_authenticate, cb_identity)
bcrypt = Bcrypt(app)


# Register the User API endpoints
from app.models.user import User
from app.resources.user import user_api
app.register_blueprint(user_api)


def register_tables():
    db.create_tables([
        User
    ])


def drop_tables():
    db.drop_tables([
        User
    ])
