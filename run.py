"""
    UFind-API.run
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import config
from app import app, register_tables


if __name__ == '__main__':
    register_tables()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
