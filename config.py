import os

class Config(object):
    SECRET_KEY = os.environment.get('SECRET_KEY') or "secret_string"