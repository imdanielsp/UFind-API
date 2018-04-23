"""
    UFind-API.subscription
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Blueprint, jsonify, request

import config
from app.models.subscription import Subscription
from app.models.category import Category
from app.models.user import User
from app.utils import make_json_response
from app import socketio

subscription_api = Blueprint('subscription', __name__,
                             url_prefix=config.URL_PREFIX)


@subscription_api.route("/category/subscribe", methods=["POST"])
def bulk_subscribe():
    """
    Subscribe to all the category in a list.
    :return:
    """
    try:
        categories = request.json["categories"]
        email = request.json["email"]
    except TypeError:
        return make_json_response(status=400)
    else:
        subs = []
        for category in categories:
            try:
                s = Subscription.subscribe(
                    email=email,
                    category_id=category
                )
                subs.append(s.to_dict_without_user())
            except Category.DoesNotExist:
                return make_json_response(status=404)
            except User.DoesNotExist:
                return make_json_response(status=404)
            except Subscription.Duplicate:
                return make_json_response(status=409)
        return jsonify(subs)


@subscription_api.route("/category/<int:category_id>/subscribe",
                        methods=["POST"])
def subscribe(category_id):
    """
    Subscribe to a category by the given ID with the user in the JSON
    :param category_id:
    :return:
    """

    try:
        subs = Subscription.subscribe(
            email=request.json["email"],
            category_id=category_id
        )
    except TypeError:
        return make_json_response(status=400)
    except Category.DoesNotExist:
        return make_json_response(status=404)
    except User.DoesNotExist:
        return make_json_response(status=404)
    except Subscription.Duplicate:
        return make_json_response(status=409)
    else:
        return jsonify(
            subs.to_dict()
        )


@subscription_api.route("/category/<int:category_id>/unsubscribe",
                        methods=["POST"])
def unsubscribe(category_id):
    """
    Unsubscribe from a category.
    :param category_id:
    :return:
    """
    try:
        Subscription.unsubscribe(
            email=request.json["email"],
            category_id=category_id
        )
    except TypeError:
        return make_json_response(status=400)
    except Subscription.NotFound:
        return make_json_response(status=404)
    else:
        return make_json_response(status=200)


@subscription_api.route("/subscription/<int:user_id>", methods=["GET"])
def get_subscriptions(user_id):
    """
    Get all subscriptions from the given user.
    :param user_id:
    :return:
    """
    return jsonify(
        list(map(lambda sub: sub.to_dict(), Subscription.by_user(user_id)))
    )


@subscription_api.route("/category/subscription/discover/<int:user_id>",
                        methods=["GET"])
def discover(user_id):
    """
    Returns users with the same interest as the user provided.
    :param user_id:
    :return:
    """
    return jsonify(
        list(
            map(lambda user: {
                "user": user[0].to_safe_dict(),
                "common": list(map(lambda cat: cat.to_dict(), user[1]))
            },
                Subscription.intersection_with(user_id))
        )
    )
