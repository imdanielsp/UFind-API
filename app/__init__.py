"""
    UFind-API.__init__.py

    This is the application level module. This file registers all the resources
    defined in the submodules.
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask
from flask_jwt import JWT
from flask_bcrypt import Bcrypt
from peewee import SqliteDatabase

import config


app = Flask(__name__)

db = SqliteDatabase(config.DATABASE_URI)
jwt = JWT(app, )
bcrypt = Bcrypt(app)


def register_tables():
    pass


def drop_tables():
    pass
