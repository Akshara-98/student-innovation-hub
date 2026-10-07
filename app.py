from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Project
from config import Config
import os
import uuid

app = Flask(__name__)
app.config.from_object(Config)

# Database Initialization
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html', page='home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('username')  # Supports username or email
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter(
            ((User.username == identifier) | (User.email == identifier)),
            User.role == role
        ).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                return redirect(url_for('company_dashboard'))
        else:
            flash('Login failed. Please check your credentials and role.')
            return redirect(url_for('login'))
    
    return render_template('index.html', page='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        college = request.form.get('college')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
            
        if email and User.query.filter_by(email=email).first():
            flash('Email address is already registered.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role,
            college=college
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
        
    return render_template('index.html', page='register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    my_projects = Project.query.filter_by(student_id=current_user.id).all()
    all_global_projects = Project.query.all()
    
    return render_template('index.html', page='student_dashboard', my_projects=my_projects, other_projects=all_global_projects)

@app.route('/student/upload', methods=['POST'])
@login_required
def upload_project():
    if current_user.role != 'student':
        return redirect(url_for('index'))
        
    title = request.form.get('title')
    description = request.form.get('description')
    phone = request.form.get('phone')
    project_url = request.form.get('project_url')
    file = request.files.get('project_image')
    
    filename = None
    if file and file.filename != '':
        filename = secure_filename(str(uuid.uuid4()) + "_" + file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    new_project = Project(
        title=title, 
        description=description, 
        phone=phone, 
        college=current_user.college or 'N/A',
        image_filename=filename,
        project_url=project_url,
        student_id=current_user.id
    )
    db.session.add(new_project)
    db.session.commit()
    
    flash('Project uploaded successfully!')
    return redirect(url_for('student_dashboard'))

@app.route('/company/dashboard')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        return redirect(url_for('index'))
    
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    
    # Create serializable version for the JS detail view with student email
    projects_data = []
    for p in all_projects:
        projects_data.append({
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'studentName': p.author.username,
            'email': p.author.email if p.author.email else 'Not provided',
            'college': p.college,
            'phone': p.phone,
            'project_url': p.project_url,
            'image': url_for('static', filename='uploads/' + p.image_filename) if p.image_filename else ''
        })
        
    return render_template('index.html', page='company_dashboard', projects=all_projects, projects_json=projects_data)

@app.route('/student/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    if current_user.role != 'student':
        return redirect(url_for('index'))
    
    project = Project.query.get_or_404(project_id)
    if project.student_id != current_user.id:
        flash('Unauthorized to delete this project.')
        return redirect(url_for('student_dashboard'))
    
    # Delete associated image if it exists
    if project.image_filename:
        try:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], project.image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
        except OSError:
            pass
            
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully.')
    return redirect(url_for('student_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
