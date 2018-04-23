"""
    UFind-API.run
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
from app import app, register_tables, socketio


if __name__ == '__main__':
    register_tables()
    socketio.run(app, port=8080, debug=True)
