# verdant_app/config.py

import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_dev')
    DATABASE_FILENAME = os.environ.get('DATABASE_FILENAME', 'verdant_app.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_FILENAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True  # Set to False in production