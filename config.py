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

DB_HOST = "i5x1cqhq5xbqtv00.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
DB_NAME = "w7emtu3wq3x97wki"
DB_USERNAME = "tghaf6moyyhyz2wr"
DB_PASSWORD = "wwiuuzv1dmats0yx"
