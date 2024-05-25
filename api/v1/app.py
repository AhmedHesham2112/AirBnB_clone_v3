#!/usr/bin/python3
'''
    This module contains variables and methods used to connect to API
'''
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', '5000'))


@app.teardown_appcontext
def teardown_app(code):
    '''
        Handles teardown
    '''
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)