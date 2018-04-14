"""
    UFind-API.__init__.py
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from flask import Response


def make_json_response(payload="", status=200, headers=None,
                       mimetype="application/json"):
    return Response(payload, status, headers, mimetype)
