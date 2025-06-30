# server/config.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # ✅ Add this

db = SQLAlchemy()
migrate = Migrate()  # ✅ Add this

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "super-secret")
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://maverick:pharaoh@localhost:5432/mkay_events"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = "Lax"

    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Add this
    CORS(app, supports_credentials=True)

    return app
