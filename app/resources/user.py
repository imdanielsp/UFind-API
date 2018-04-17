"""
    UFind-API.user
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, jsonify, request

import config
from app.models.user import User
from app.utils import make_json_response

user_api = Blueprint('user', __name__, url_prefix=config.URL_PREFIX)


@user_api.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
        Return a JSON version of a User.
    :param user_id:
    :return: Response
    """

    try:
        user = User.get_user_by_id(user_id)
    except Exception:
        return make_json_response(status=404)
    else:
        # Marshall the user, and make a json response
        return jsonify(
            user.to_safe_dict()
        )


@user_api.route("/user", methods=["POST"])
def create_user():
    """
        Creates a user given by the JSON in the request.
    :return: Response
    """

    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        password = request.json["password"]
        bio = request.json["bio"]
        profile_picture = request.json["profile_picture"].encode()
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            user = User.safe_create(first_name, last_name, email, password,
                                    bio, profile_picture)
        except User.DuplicateUser:
            return make_json_response(status=409)
        else:
            return jsonify(user)


@user_api.route("/login", methods=["POST"])
def login():
    """
        Check email and password in database, returns JWT.
    :return: Response
    """

    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            if User.check_password_for(email, password):
                return jsonify(
                    User.get_user_by_email(email).to_dict_with_token()
                )
            return make_json_response(status=403)
        except User.NotFound:
            return make_json_response(status=404)


@user_api.route("/user/verify/email", methods=["POST"])
def sign_up_verify():
    """
    Verify that the email isn't a duplicate.
    :return:
    """
    try:
        email = request.json["email"]
    except TypeError:
        return make_json_response(status=400)
    else:
        if User.is_email_duplicate(email):
            return make_json_response(status=409)
        else:
            return make_json_response(status=200)


@user_api.route("/user/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    """
        Update the given User by the ID with the user structure specified in the
        JSON field of the request.
    :param user_id:
    :return: Response
    """
    try:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            user = User.get_user_by_id(user_id)
        except Exception:
            return make_json_response(status=404)
        else:
            user.update_with(first_name, last_name, email, password)

            return jsonify(
                user.to_safe_dict()
            )
