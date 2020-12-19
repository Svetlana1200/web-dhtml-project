import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    SECRET_KEY = os.urandom(50)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CATS_DIR = os.path.join(basedir, "app", "static", "cats")
