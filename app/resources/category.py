"""
    UFind-API.cetegory
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, jsonify, request

import config
from app.models.category import Category
from app.utils import make_json_response

category_api = Blueprint('category', __name__, url_prefix=config.URL_PREFIX)


@category_api.route("/category")
@category_api.route("/category/<int:category_id>", methods=["GET"])
def get_category(category_id=None):
    """
    Return a JSON version of the category.
    :param category_id:
    :return: Response
    """
    try:
        category = Category.by_id(category_id)
    except Exception:
        return jsonify(
            Category.all()
        )
    else:
        return jsonify(
            category.to_dict()
        )


@category_api.route("/category", methods=["POST"])
def create_category():
    """
    Creates a category given by the JSON in the request.
    :return:
    """
    try:
        name = request.json["name"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            category = Category.create(name=name)
        except Category.DuplicateCategory:
            return make_json_response(status=409)
        else:
            return jsonify(
                category.to_dict()
            )


@category_api.route("/category/<int:category_id>", methods=["PUT"])
def edit_category(category_id):
    """
    Update the given category by the ID.
    :return:
    """
    try:
        name = request.json["name"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            category = Category.by_id(category_id)
        except Exception:
            return make_json_response(status=404)
        else:
            category.update_with(name)

            return jsonify(
                category.to_dict()
            )
