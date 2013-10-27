from flask import Blueprint


bp = api_blueprint = Blueprint('api', __name__)

@bp.route('/')
def index():
    return "This is the root of the API endpoint"


@bp.route('/example')
def example():
    return "This is an /example url for the API"
