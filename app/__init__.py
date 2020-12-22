from flask import (
    Blueprint,
    flash, g,
    redirect,
    render_template,
    request, session,
    url_for,
    abort,
    Flask, jsonify
)
from config import ConfigManager, INIManager
from database import DAO
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import json
from model.item import Item, User

db = SQLAlchemy()
ini_manger = INIManager("app.ini")

def create_app(env=None):
  from app.auth import auth, login_required
  # from app.db_util import init_db, init_db_command

  app = Flask(__name__)
  app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_TRACK_MODIFICATIONS = False
  )
  DATABASE=ini_manger.read_ini("Database", "Database_Name")
  app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../{DATABASE}"
  app.register_blueprint(auth)
  db.init_app(app)
  # app.cli.add_command(init_db_command)
  
  @app.route('/', methods=['POST', 'GET'])
  @login_required
  def index():
    if request.method == 'POST':
      pass
    items = db.session.query(Item).all()
    
    return render_template('index.html', items=items)

  @app.route('/user')
  def user():
    user = db.session.query(User).first().__dict__
    user.pop('_sa_instance_state')
    user.pop('_password')
    print(user)
    return jsonify(user)

  return app