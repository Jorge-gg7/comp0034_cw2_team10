from flask import Flask
from flask_login import LoginManager
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

    db.init_app(app)
    login_manager.init_app(app)
    csrf_protect.init_app(app)

    with app.app_context():
        # Import Dash application
        from dash_app.index import init_dashboard
        app = init_dashboard(app)

    return app