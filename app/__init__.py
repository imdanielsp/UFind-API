"""
    UFind-API.__init__.py

    This is the application level module. This file registers all the resources
    defined in the submodules.
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from flask_bcrypt import Bcrypt
from peewee import MySQLDatabase

import config
from app.auth import cb_authenticate, cb_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.SECRET_KEY

db = MySQLDatabase(config.DB_NAME, user=config.DB_USERNAME,
                   password=config.DB_PASSWORD, host=config.DB_HOST, port=3306)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
socketio = SocketIO(app=app, ping_timeout=2, ping_interval=2)

from app.resources import chat

# Register the User API endpoints
from app.models.user import User
from app.resources.user import user_api
app.register_blueprint(user_api)

# Register the Category API endpoints
from app.models.category import Category
from app.resources.category import category_api
app.register_blueprint(category_api)

# Register the Subscription API endpoints
from app.models.subscription import Subscription
from app.resources.subscription import subscription_api
app.register_blueprint(subscription_api)

# Register the Connection API endpoints
from app.models.connection import Connection
from app.resources.connection import connection_api
app.register_blueprint(connection_api)

# Register the Chat API endpoints
from app.models.conversation import Conversation
from app.models.message import Message
from app.resources.chat import chat_api
app.register_blueprint(chat_api)


def register_tables():
    db.create_tables([
        User,
        Category,
        Subscription,
        Connection,
        Conversation,
        Message
    ])


def drop_tables():
    db.drop_tables([
        User
    ])
