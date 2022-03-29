from flask import Blueprint

community_bp = Blueprint('community', __name__, url_prefix='/community')

@community_bp.route('/')
def main():
    return "This is the authentication section of the web app"