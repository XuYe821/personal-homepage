from flask import Flask,render_template,session,redirect,url_for,flash
# from flask_script import Manager,Server
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY']='test'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:xzwhf123@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
bootstrap=Bootstrap(app)

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
    name = StringField('Name?',validators=[DataRequired()]) 
    # 新增 SelectField，coerce=int 确保表单返回的是整数ID
    major = SelectField('Major', coerce=int)
    submit = SubmitField('Submit') 
class EditForm(NameForm):
    submit = SubmitField("Edit") 
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
@app.route("/",methods=['GET','POST'])
def index():
    studs = Student_Info.query.all()
    majors = Major.query.all() # 查询所有专业
    return render_template('index.html',studs=studs, majors=majors)
@app.route("/major/<int:major_id>")
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('index.html', studs=studs, majors=majors)
@app.route("/new",methods=['GET','POST'])
def new_stud():
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
        return redirect(url_for('index')) 
    return render_template("new_student.html",form=form)
@app.route("/edit/<int:stu_id>",methods=["GET","POST"])
def edit_stud(stu_id):
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
        return redirect(url_for('index'))
    form.id.data=stud.student_id
    form.name.data = stud.student_name
    # 页面加载时，设置下拉框的默认选中项
    if stud.major:
        form.major.data = stud.major_id
    return render_template('edit_info.html',form=form) # 注意使用修复后的模板名
@app.route("/delete/<int:stud_id>",methods=["GET","POST"])
def del_stud(stud_id):
    stud = Student_Info.query.get(stud_id)
    db.session.delete(stud)
    db.session.commit()
    flash('Delete 1 student')
    return redirect(url_for('index'))
if __name__=='__main__':
    app.run(debug=True)