from flask import Blueprint, request, session, jsonify
from models import db, Event

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["POST"])
def create_event():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    event = Event(
        title=data["title"],
        description=data["description"],
        date=data["date"],
        user_id=user_id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@events_bp.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events]), 200
