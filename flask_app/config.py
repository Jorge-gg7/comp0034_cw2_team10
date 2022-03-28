from pathlib import Path


class Config(object):
    """ Sets the Flask base configuration that is common to all environments. """
    DEBUG = False
    SECRET_KEY = '7ybSP3F4x8PVjetxQrY49w'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = Path(__file__).parent.parent.joinpath("datasets")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('datasets.sqlite'))


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True