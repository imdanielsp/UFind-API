"""
    UFind-API.user
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.

    Note: We are using peewee as our ORM.
"""
import datetime

from peewee import *

from app import bcrypt
from . import BaseModel
from flask_jwt_extended import create_access_token


class User(BaseModel):
    """
        Representation of an user.
    """
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField()
    bio = CharField()
    profile_image = BlobField()
    joined = DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "<User: {} {}>".format(self.first_name, self.last_name)

    @staticmethod
    def safe_create(first_name: str, last_name: str, email: str, password: str,
                    bio: str, profile_image: bytes):
        """
            Create a user and hash the password before storing it in the
            database.
        :param first_name:
        :param last_name:
        :param email:
        :param password:
        :param bio:
        :param profile_image:
        :return:
        """
        try:
            user = User.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=bcrypt.generate_password_hash(password),
                bio=bio,
                profile_image=profile_image
            )
        except IntegrityError:
            raise User.DuplicateUser

        return user.to_dict_with_token()

    @staticmethod
    def check_password_for(email: str, password: str) -> bool:
        user = User.get_user_by_email(email)
        return bcrypt.check_password_hash(user.password, password)

    @staticmethod
    def get_user_by_id(user_id: int):
        try:
            return User.get(User.id == user_id)
        except DoesNotExist:
            raise User.NotFound

    @staticmethod
    def get_user_by_email(email: str):
        try:
            return User.get(User.email == email)
        except DoesNotExist:
            raise User.NotFound

    def update_with(self, first_name, last_name, email, password, bio,
                    profile_image):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.bio = bio
        self.profile_image = profile_image

        self.save()

    def to_safe_dict(self):
        user = self.to_dict()
        user.pop("password")
        return user

    def to_dict_with_token(self):
        user = self.to_safe_dict()
        user.pop("profile_image")
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
            "password": self.password,
            "bio": self.bio,
            "profile_image": self.profile_image.decode()
        }

    class NotFound(DoesNotExist):
        pass

    class DuplicateUser(IntegrityError):
        pass
