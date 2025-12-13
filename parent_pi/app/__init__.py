from flask import Flask
from . import routes


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    
    routes.init_master_bp(app) # Init blueprint config
    app.register_blueprint(routes.master_bp) # Register blueprint

    return app
