  # 稍后在 __init__.py 中定义 db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
# (注意：login_manager.user_loader 也会移到这里或 __init__)
# from . import login_manager # 稍后在 __init__.py 中定义 login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.String(16), default='guest') # (如果实现了挑战任务)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship('Student_Info', backref='major', lazy='dynamic')

class Student_Info(db.Model):
    __tablename__ = 'student_info'
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.Text)
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))