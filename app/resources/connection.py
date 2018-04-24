"""
    UFind-API.connection
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, jsonify, request

import config
from app.models.connection import Connection
from app.models.user import User
from app.utils import make_json_response

connection_api = Blueprint('connection', __name__, url_prefix=config.URL_PREFIX)


@connection_api.route("/connection", methods=["POST"])
def create_connection():
    """
    Create a connection between the two users.
    :return:
    """
    try:
        user_a_id = request.json["user_a"]
        user_b_id = request.json["user_b"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            user_a = User.get_by_id(user_a_id)
            user_b = User.get_by_id(user_b_id)
        except User.DoesNotExist:
            return make_json_response(status=404)
        else:
            try:
                conn = Connection.connect(user_a, user_b)
            except Connection.Duplicate:
                return make_json_response(status=409)
            else:
                return jsonify(conn.to_dict())


@connection_api.route("/connection/verify", methods=["POST"])
def verify_connection():
    """
    Verify if two users are connected.
    :return:
    """
    try:
        user_a_id = request.json["user_a"]
        user_b_id = request.json["user_b"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            user_a = User.get_by_id(user_a_id)
            user_b = User.get_by_id(user_b_id)
        except User.DoesNotExist:
            return make_json_response(status=404)
        else:
            if Connection.already_connected(user_a, user_b):
                return make_json_response(status=200)
            else:
                return make_json_response(status=204)


@connection_api.route("/connection/<int:user_id>")
def get_connection_by_user(user_id):
    """
    Returns the
    :param user_id:
    :return:
    """
    return jsonify(Connection.by_user(user_id))
