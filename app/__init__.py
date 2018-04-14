"""
    UFind-API.__init__.py

    This is the application level module. This file registers all the resources
    defined in the submodules.
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, blueprints
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)
from flask_bcrypt import Bcrypt
from peewee import SqliteDatabase

import config
from app.auth import cb_authenticate, cb_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY

db = SqliteDatabase(config.DATABASE_URI)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register the User API endpoints
from app.models.user import User
from app.resources.user import user_api
app.register_blueprint(user_api)

# Register the Category API endpoints
from app.models.category import Category
from app.resources.category import category_api
app.register_blueprint(category_api)


def register_tables():
    db.create_tables([
        User,
        Category
    ])


def drop_tables():
    db.drop_tables([
        User
    ])
