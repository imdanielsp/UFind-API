"""
    UFind-API.user
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import datetime

from peewee import *

from app import bcrypt
from . import BaseModel
from flask_jwt_extended import (create_access_token)

class User(BaseModel):
    """
        Representation of an user.
    """
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    joined = DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "<User: {} {}>".format(self.first_name, self.last_name)

    @staticmethod
    def safe_create(first_name: str, last_name: str, email: str, password: str):
        """
            Create a user and hash the password before storing it in the
            database.
        :param first_name:
        :param last_name:
        :param email:
        :param password:
        :return:
        """
        user = User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=bcrypt.generate_password_hash(password)
        )

        return user.generate_token()

    @staticmethod
    def check_password_for(email: str, password: str) -> bool:
        user = User.get(User.email == email)
        return bcrypt.check_password_hash(user.password, password)

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.get(User.id == user_id)

    @staticmethod
    def get_user_by_email(email: str):
        return User.get(User.email == email)

    def update_with(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

        self.save()

    def to_safe_dict(self):
        user = self.to_dict()
        user.pop("password")
        return user
    
    def generate_token(self):
        user = self.to_safe_dict()
        user['access_token'] = create_access_token(identity=user)
        return user

    def to_dict(self):
        """
            Make this object a dictionary.
        :return: dict
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }

    class NotFound(DoesNotExist):
        pass
