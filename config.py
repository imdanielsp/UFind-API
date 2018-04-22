"""
    UFind-API.config
    
    :copyright: (c) Feb 2018 by Daniel Santos.
    :license: BSD, see LICENSE for more details.
"""
import os

API_VERSION = 1
URL_PREFIX = "/ufind/api/v{}".format(API_VERSION)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Runtime
HOST = "127.0.0.1"
PORT = 8080

DEBUG = True

SECRET_KEY = "2dc27eab485446a7b30016381f5fcfd4"

DATABASE_URI = "{}/UFind.db".format(BASE_DIR)

DB_HOST = "us-cdbr-iron-east-05.cleardb.net"
DB_NAME = "heroku_8b591c6ac33c025"
DB_USERNAME = "b5e4865df413e2"
DB_PASSWORD = "8472932d"
