from configparser import ConfigParser
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

__all__ = ['app', 'db']

app = Flask(__name__)

cfg = ConfigParser()
cfg.read(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                 'alembic.ini')
)

app.config['SQLALCHEMY_DATABASE_URI'] = cfg.get('alembic', 'sqlalchemy.url')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
