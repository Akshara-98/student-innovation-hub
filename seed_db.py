from app import app, db
from models import User, Project
from werkzeug.security import generate_password_hash

def seed_data():
    with app.app_context():
        # Drop and recreate for a clean slate
        db.drop_all()
        db.create_all()
        
        # Create Student
        student = User(
            username='jdoe',
            email='jdoe@techinstitute.edu',
            password=generate_password_hash('student1', method='pbkdf2:sha256'),
            role='student',
            college='Tech Institute'
        )
        
        # Create Company
        company = User(
            username='innovators_inc',
            email='contact@innovators.com',
            password=generate_password_hash('company1', method='pbkdf2:sha256'),
            role='company'
        )
        
        db.session.add(student)
        db.session.add(company)
        db.session.commit()
        
        # Create Project
        project = Project(
            title='Smart Traffic System',
            description='An AI-powered traffic management system using computer vision to optimize signal timings in real-time.',
            phone='1234567890',
            college='Tech Institute',
            project_url='https://github.com/jdoe/smart-traffic',
            student_id=student.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        print("Database seeded with 'jdoe' (student1) and 'innovators_inc' (company1)!")

if __name__ == '__main__':
    seed_data()
