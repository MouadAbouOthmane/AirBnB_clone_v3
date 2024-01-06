#!/usr/bin/python3
"""app module"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    """teardown appcontext"""
    storage.close()


if __name__ == '__main__':

    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    HBNB_API_HOST = HBNB_API_HOST if HBNB_API_HOST else '0.0.0.0'
    HBNB_API_PORT = HBNB_API_PORT if HBNB_API_PORT else '5000'

    app.run(host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True)
