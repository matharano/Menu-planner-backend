from flask import Flask

from .api import api
from .utils import init_logging

log = init_logging('backend', 'DEBUG')

def create_app():
    log.info('app init')
    app = Flask(__name__)
    app.config['RESTX_MASK_SWAGGER'] = False
    api.init_app(app)
    # register_models(api)
    return app