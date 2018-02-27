"""
    UFind-API.post
    
    :copyright: (c) Feb 2018 by Serey Morm.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, jsonify, request

import config
from app.models.post import Post
from app.utils import make_json_response
from flask_jwt_extended import (create_access_token)

post_api = Blueprint('post', __name__, url_prefix=config.URL_PREFIX)

@post_api.route("/post", methods=["POST"])
def create_post():
    """
        Creates a post given by the JSON in the request.
    :return: Response
    """
    try:
        title = request.json["title"]
        description = request.json["description"]
        category = request.json["category"]
        date = request.json["date"]
        user_id = request.json["user_id"]
    except KeyError:
        return make_json_response(status=400)
    else:
      try:
        post = Post.create(
          title=title,
          description=description,
          category=category,
          date=date,
          author=user_id
        )
      except Exception as e:
        return make_json_response(status=409)
    return jsonify(post.to_dict())


@post_api.route("/post/<int:post_id>", methods=["GET"])
def get_post(post_id):
    """
        Return a JSON version of a post.
    :param post_id:
    :return: Response
    """

    try:
        post = Post.get_post_by_id(post_id)
    except Exception:
        return make_json_response(status=404)
    else:
        return jsonify(post.to_dict())


