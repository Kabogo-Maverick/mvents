# server/app.py

from flask import Flask
from flask_cors import CORS
from config import create_app, db
from auth.routes import auth_bp
from events.routes import events_bp

# Create the app from factory
app = create_app()
app.static_folder = 'static'



# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(events_bp, url_prefix="/events")

# CORS already handled inside config.py -> create_app()

# Create tables
with app.app_context():
    db.create_all()
