from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abdjkasvfhj'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:xzwhf123@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = '请登录！'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

db = SQLAlchemy(app)
USER_ID_START = 1000
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(16), nullable=False, default='guest')
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Major(db.Model):
    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(100), unique=True, nullable=False)
    # 定义“一对多”关系中的“一”
    # 'students' 是反向引用的名称，'major' 是在 Student_Info 中定义的 backref 名称
    students = db.relationship('Student_Info', backref='major', lazy='dynamic')
    def __repr__(self):
        return f'<Major {self.major_name}>'

class Student_Info(db.Model):
    __tablename__='student_info'
    student_id = db.Column(db.Integer,primary_key=True)
    student_name = db.Column(db.Text) 
    # 新增外键列
    major_id = db.Column(db.Integer, db.ForeignKey('majors.id'))
class NameForm(FlaskForm):
    id = IntegerField('Id') 
    name = StringField('Name',validators=[DataRequired()]) 
    # 新增 SelectField，coerce=int 确保表单返回的是整数ID
    major = SelectField('Major', coerce=int)
    submit = SubmitField('Submit') 
class EditForm(NameForm):
    submit = SubmitField("Edit") 
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_next_user_id():
    last_user = User.query.order_by(User.id.desc()).first()
    if last_user:
        return last_user.id + 1
    else:
        return USER_ID_START

def new_user(username, email, password):
    id = get_next_user_id()
    user = User(id=id, username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember'))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='用户名或密码错误')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']
        if password != confirm_password:
            return render_template('signup.html', error='两次密码不一致')
        else:
            new_user(username, email, password)
            return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    studs = Student_Info.query.all()
    majors = Major.query.all() # 查询所有专业
    return render_template('dashboard.html',studs=studs, majors=majors)

@app.route("/major/<int:major_id>")
@login_required
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('dashboard.html', studs=studs, majors=majors)

@app.route("/new",methods=['GET','POST'])
@login_required
def new_stud():
    if current_user.role != 'admin':
        flash('您没有权限添加学生记录')
        return redirect(url_for('dashboard'))
    form = NameForm()
    # 动态填充选项：(value, label) 
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        # 通过ID获取选择的 Major 对象
        major_obj = Major.query.get(form.major.data)
        newstud = Student_Info(student_id=id, student_name=name, major=major_obj) # 使用 major 属性关联
        db.session.add(newstud)
        db.session.commit() 
        flash("a new student record is saved") 
        return redirect(url_for('dashboard')) 
    return render_template("new_student.html",form=form)

@app.route("/edit/<int:stu_id>",methods=["GET","POST"])
@login_required
def edit_stud(stu_id):
    if current_user.role != 'admin':
        flash('您没有权限编辑学生记录')
        return redirect(url_for('dashboard'))
    form=EditForm()
    stud = Student_Info.query.get(stu_id)
    # 同样需要动态填充选项
    form.major.choices = [(m.id, m.major_name) for m in Major.query.order_by('major_name').all()]
    if form.validate_on_submit():
        stud.student_id=form.id.data
        stud.student_name = form.name.data
        stud.major = Major.query.get(form.major.data) # 更新关联
        db.session.commit() 
        flash('The record is updated') 
        return redirect(url_for('dashboard'))
    form.id.data=stud.student_id
    form.name.data = stud.student_name
    # 页面加载时，设置下拉框的默认选中项
    if stud.major:
        form.major.data = stud.major_id
    return render_template('edit_info.html',form=form) # 注意使用修复后的模板名

@app.route("/delete/<int:stu_id>",methods=["GET","POST"])
@login_required
def delete_stud(stu_id):
    if current_user.role != 'admin':
        flash('您没有权限删除学生记录')
        return redirect(url_for('dashboard'))
    stud = Student_Info.query.get(stu_id)
    db.session.delete(stud)
    db.session.commit() 
    flash('The record is deleted') 
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True)