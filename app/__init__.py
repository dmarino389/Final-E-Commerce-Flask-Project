from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .models import db
from flask_login import LoginManager
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app.models import db
from app.models import User

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



from app import routes

