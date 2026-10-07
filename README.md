# Innovation Hub 🚀

**Innovation Hub** is a web platform connecting student innovators and companies. Students can showcase their science fair and startup projects, while companies can explore innovations, review student details, and connect directly via email or call.

---

## ✨ Features

- **Single Frontend Architecture**: Entire UI is consolidated into `templates/index.html`.
- **Student Portal**:
  - Registration with Email, Username, Password, and College.
  - Login via Username or Email.
  - Upload projects with Title, Description/PMF, Phone, Project Demo/Repo URL, and Images.
  - View personal projects and explore global student innovations.
- **Company Portal**:
  - Live Innovation Feed with search and filter.
  - Interactive Project Detail view.
  - Direct **Send Email** button (`mailto:`) with pre-composed subject and message to contact student innovators directly.
  - Direct **Call Student** button.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug
- **Frontend**: HTML5, CSS3 (Glassmorphism design), FontAwesome, JavaScript
- **Database**: SQLite

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

### 2. Seed Database (Demo Data)
```bash
python seed_db.py
```
*Default student credentials:* `jdoe` / `student1` (or email: `jdoe@techinstitute.edu`)  
*Default company credentials:* `innovators_inc` / `company1` (or email: `contact@innovators.com`)

### 3. Run the App
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

---

## 📦 Pushing to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Innovation Hub with unified frontend and email outreach"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

