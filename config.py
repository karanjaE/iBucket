import os
base_dir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ["SECRET_KEY"]


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    DB_URL = os.environ["DB_URL"]

class TestingConf(Config):
    TESTING = True
    DB_URL = os.environ["TEST_DB_URL"]


class DevelopmentConf(Config):
    DEBUG = True
    DEVELOPMENT = True


class ProductionConf(Config):
    DEBUG = False
