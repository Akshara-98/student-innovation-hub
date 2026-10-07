from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'student' or 'company'
    college = db.Column(db.String(200), nullable=True) # For students
    
    # Relationship: A student can have multiple projects
    projects = db.relationship('Project', backref='author', lazy=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    college = db.Column(db.String(200), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)
    project_url = db.Column(db.String(500), nullable=True) # New field for demo/repo link
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
