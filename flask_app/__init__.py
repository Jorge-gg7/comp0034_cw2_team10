import dash
import dash_bootstrap_components as dbc
import pandas as pd
from flask import Flask
from flask.helpers import get_root_path
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf_protect = CSRFProtect()
csrf_protect._exempt_views.add('dash.dash.dispatch')


def create_app(config_classname):
    """
    Initialise and configure the Flask application.
    :type config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_classname)

    register_dashapp(app)

    db.init_app(app)
    csrf_protect.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    with app.app_context():
        db.Model.metadata.reflect(bind=db.engine)

    from flask_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from flask_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    return app

def register_dashapp(app):
    """ Registers the Dash app in the Flask app and make it accessible on the route /dashboard/ """
    from dash_app import layout
    from dash_app.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/map/',
                         assets_folder=get_root_path(__name__) + '/map/assets/',
                         meta_tags=[meta_viewport],
                         external_stylesheets=[dbc.themes.LUX])

    with app.app_context():
        dashapp.title = 'Map'
        dashapp.layout = layout.layout
        register_callbacks(dashapp)

    # Protects the views with Flask-Login
    _protect_dash_views(dashapp)

def _protect_dash_views(dash_app):
    """ Protects Dash views with Flask-Login"""
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
