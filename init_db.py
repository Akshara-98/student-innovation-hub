from app import app, db
from models import User, Project
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Clear existing data and recreate tables
        db.drop_all()
        db.create_all()
        print("Database cleared and initialized successfully!")

if __name__ == '__main__':
    init_db()
