from flask import Flask

from .api import api
from .utils import init_logging

log = init_logging('backend', 'DEBUG')

def create_app():
    log.info('app init')
    app = Flask(__name__)
    api.init_app(app)
    return app