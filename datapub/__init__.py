from flask import Flask

from .models import db
from .blueprints.api import api_blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# todo: load configuration from config file
db.init_app(app)
app.register_blueprint(api_blueprint, url_prefix='/api/1')
