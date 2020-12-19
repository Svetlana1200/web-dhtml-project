from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import BaseConfig

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migration = Migrate(app, db, render_as_batch=True)
lm = LoginManager(app)

from app import views, models
