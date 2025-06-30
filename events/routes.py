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



# POST /events/<id>/add-to-mine — duplicate an admin event into current user's events
@events_bp.route("/<int:id>/add-to-mine", methods=["POST"])
def add_to_my_events(id):
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "Unauthorized"}, 401

    original_event = Event.query.get_or_404(id)

    # Only allow duplicating events made by admins
    original_creator = User.query.get(original_event.user_id)
    if not original_creator or not original_creator.is_admin:
        return {"error": "Only admin events can be copied"}, 403

    # Duplicate the event but assign to current user
    copied = Event(
        title=original_event.title,
        description=original_event.description,
        date=original_event.date,
        image_url=original_event.image_url,
        user_id=user_id
    )

    db.session.add(copied)
    db.session.commit()
    return jsonify(copied.to_dict()), 201



# events/routes.py

# @events_bp.route("/<int:event_id>/add-to-mine", methods=["POST"])
# def clone_event_to_user(event_id):
#     user_id = session.get("user_id")
#     if not user_id:
#         return {"error": "Unauthorized"}, 401

#     original = Event.query.get_or_404(event_id)

#     # Clone the event for this user
#     new_event = Event(
#         title=original.title,
#         description=original.description,
#         date=original.date,
#         image_url=original.image_url,
#         user_id=user_id  # Now belongs to current user
#     )

#     db.session.add(new_event)
#     db.session.commit()

#     return jsonify(new_event.to_dict()), 201
