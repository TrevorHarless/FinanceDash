"""
This file is for all routing purposes.
"""
from application import app

@app.route("/")

@app.route("/index")
def index():
    return "<h1>Hello!</h1>"