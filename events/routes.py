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

# 🔁 UPDATE EVENT
@events_bp.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if event.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.date = data.get("date", event.date)

    db.session.commit()
    return jsonify(event.to_dict()), 200

# ❌ DELETE EVENT
@events_bp.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    if event.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200
