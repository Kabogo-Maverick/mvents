# seed.py
from config import app, db

with app.app_context():
    print("🌱 Seeding DB...")
    db.drop_all()
    db.create_all()
    # Add test data later
    print("🌱 DB seeded successfully!")