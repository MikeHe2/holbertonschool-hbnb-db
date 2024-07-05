"""
This module exports configuration classes for the Flask application.

- DevelopmentConfig
- TestingConfig
- ProductionConfig

"""

from abc import ABC
import os


class Config(ABC):
    """
    Initial configuration settings
    This class should not be instantiated directly
    """

    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configuration settings
    This configuration is used when running the application locally

    This is useful for development and debugging purposes.

    To check if the application is running in development mode, you can use:
    ```
    app = Flask(__name__)

    if app.debug:
        # Do something
    ```
    """

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///hbnb_dev.db")
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration settings
    This configuration is used when running tests.
    You can enabled/disable things across the application

    To check if the application is running in testing mode, you can use:
    ```
    app = Flask(__name__)

    if app.testing:
        # Do something
    ```

    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """
    Production configuration settings
    This configuration is used when you create a
    production build of the application

    The debug or testing options are disabled in this configuration.
    """

    TESTING = False
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqldb://root:""@localhost/hbnb_prod"
    )