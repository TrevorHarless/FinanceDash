from flask import Flask
from config import Config
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object(Config)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


from application import routes

