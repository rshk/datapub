from flask import Flask

from .models import db
from .blueprints.api import api_blueprint


app = Flask(__name__)

## Default configuration
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

## Load configuration from config file.
## The environment variable should point (path) to a Python
## module containing the configuration.
app.config.from_envvar('DATAPUB_SETTINGS', silent=True)

## Register the application within the database connector
db.init_app(app)

## Register blueprints
app.register_blueprint(api_blueprint, url_prefix='/api/1')

## ``app.run()`` can be used to start the server.
## We are doing that in the ``run.py`` script.
