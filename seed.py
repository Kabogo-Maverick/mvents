# seed.py
from config import create_app, db
from models import Event, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Clear
    Event.query.delete()
    User.query.delete()

    # Users
    admin = User(username="admin", is_admin=True, password_hash=generate_password_hash("adminpass"))
    user = User(username="user", is_admin=False, password_hash=generate_password_hash("userpass"))
    db.session.add_all([admin, user])
    db.session.commit()

    # Events
    demo_events = [
        Event(
            title="Public Launch",
            description="Launching our event portal",
            date="2025-07-01",
            image_url="http://localhost:5000/static/ima1.jpeg",
            user_id=admin.id
        ),
        Event(
            title="User Meetup",
            description="Networking and games",
            date="2025-07-05",
            image_url="http://localhost:5000/static/ima2.jpeg",
            user_id=user.id
        ),
    ]

    db.session.add_all(demo_events)
    db.session.commit()
    print("✅ Seeded users and events with full image URLs")
