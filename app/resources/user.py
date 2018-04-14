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


@user_api.route("/users", methods=["POST"])
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
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            user = User.safe_create(first_name, last_name, email, password, bio)
        except User.DuplicateUser:
            return make_json_response(status=409)
        else:
            return jsonify(
                user.to_safe_dict()
            )


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
