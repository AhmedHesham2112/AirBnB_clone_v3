#!/usr/bin/python3
""" initializes view of directory  """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
