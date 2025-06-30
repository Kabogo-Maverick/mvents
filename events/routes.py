from flask import Blueprint, request, session, jsonify
from models import db, Event, User

events_bp = Blueprint("events", __name__, url_prefix="/events")

# Admin: Create public event
@events_bp.route("", methods=["POST"])
def create_event():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)
    if not user.is_admin:
        return {"error": "Forbidden: Admins only can create events"}, 403

    data = request.get_json()

    event = Event(
        title=data.get("title"),
        description=data.get("description"),
        date=data.get("date"),
        image_url=data.get("image_url"),  # ✅ NEW
        user_id=user_id
    )

    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

# GET public events (admin-created)
@events_bp.route("", methods=["GET"])
def get_events():
    admins = User.query.filter_by(is_admin=True).all()
    admin_ids = [admin.id for admin in admins]
    events = Event.query.filter(Event.user_id.in_(admin_ids)).all()
    return jsonify([e.to_dict() for e in events]), 200

# GET personal events
@events_bp.route("/mine", methods=["GET"])
def my_events():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    events = Event.query.filter_by(user_id=user_id).all()
    return jsonify([e.to_dict() for e in events]), 200

# PATCH / DELETE event
@events_bp.route("/<int:id>", methods=["PATCH", "DELETE"])
def modify_event(id):
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    user = User.query.get(user_id)
    event = Event.query.get_or_404(id)

    # Only owner or admin can edit/delete
    if event.user_id != user_id and not user.is_admin:
        return {"error": "Forbidden"}, 403

    if request.method == "PATCH":
        data = request.get_json()
        event.title = data.get("title", event.title)
        event.description = data.get("description", event.description)
        event.date = data.get("date", event.date)
        event.image_url = data.get("image_url", event.image_url)  # ✅ FIXED placement
        db.session.commit()
        return jsonify(event.to_dict()), 200

    if request.method == "DELETE":
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200
