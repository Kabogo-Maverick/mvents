# server/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret")
    SQLALCHEMY_DATABASE_URI = "postgresql://maverick:pharaoh@localhost:5432/mkay_events"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
