"""
    UFind-API.chat
    
    :copyright: (c) Apr 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import json
from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room

import config
from app import socketio
from app.utils import make_json_response
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message

chat_api = Blueprint("chat", __name__, url_prefix=config.URL_PREFIX)


@chat_api.route("/conversation", methods=["POST"])
def create_conversation():
    """
    Create conversation, if already exists sends old message back.
    :return:
    """
    try:
        user_a = request.json["user_a"]
        user_b = request.json["user_b"]
    except KeyError:
        return make_json_response(status=400)
    else:
        try:
            conv = Conversation.by_user(user_a, user_b)
        except Conversation.NotFound:
            try:
                conv = Conversation.make_between(user_a, user_b)
            except User.NotFound:
                return make_json_response(status=404)
            else:
                return jsonify(
                    {
                        "conversation": conv.to_dict(),
                        "messages": []
                    }
                )
        else:
            return jsonify(
                {
                    "conversation": conv.to_dict(),
                    "messages": Message.by_conversation(conv)
                }
            )


@socketio.on("text", namespace=config.URL_PREFIX + "/chat")
def rcv_message(message):
    msg = json.loads(message)

    user = User.get_by_id(msg["sender_id"])

    emit('message', {
        'msg': msg["msg"],
        'sender': user.to_dict_without_picture(),
        'conversation_id': msg['conversation_id']
    })

    Message.add(
        msg.get("conversation_id"),
        msg.get("sender_id"),
        msg.get("msg")
    )
