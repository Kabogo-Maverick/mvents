from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS

from config import Config
from models import db
from auth import auth_bp
from events import events_bp

app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)
Session(app)
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(events_bp)

@app.route("/")
def index():
    return {"message": "Mkay Events Backend Running!"}

if __name__ == "__main__":
    app.run(port=5000, debug=True)
