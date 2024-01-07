#!/usr/bin/python3
"""views init"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

import api.v1.views.states
import api.v1.views.index
