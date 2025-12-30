from flask import render_template, redirect, url_for, flash
from . import main
from .. import db
from ..models import Student_Info, Major
from ..forms import NameForm, EditForm, DeleteForm
from flask_login import login_required, current_user # (用于权限控制)


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    studs = Student_Info.query.all()
    majors = Major.query.all() # 查询所有专业
    return render_template('dashboard.html',studs=studs, majors=majors)

@main.route("/major/<int:major_id>")
@login_required
def filter_by_major(major_id):
    # 找到被点击的专业
    major = Major.query.get_or_404(major_id)
    # 使用 'major' 关系的反向查询 'students'
    studs = major.students.all()
    # 复用 index.html 模板，但只传入筛选后的学生
    majors = Major.query.all() # 筛选页面也需要专业列表
    return render_template('dashboard.html', studs=studs, majors=majors)

@main.route("/new",methods=['GET','POST'])
@login_required
def new_stud():
    if current_user.role != 'admin':
        flash('您没有权限添加学生记录')
        return redirect(url_for('main.dashboard'))
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
        return redirect(url_for('main.dashboard')) 
    return render_template("new_student.html",form=form)

@main.route("/edit/<int:stu_id>",methods=["GET","POST"])
@login_required
def edit_stud(stu_id):
    if current_user.role != 'admin':
        flash('您没有权限编辑学生记录')
        return redirect(url_for('main.dashboard'))
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
        return redirect(url_for('main.dashboard'))
    form.id.data=stud.student_id
    form.name.data = stud.student_name
    # 页面加载时，设置下拉框的默认选中项
    if stud.major:
        form.major.data = stud.major_id
    return render_template('edit_info.html',form=form) # 注意使用修复后的模板名

@main.route("/delete/<int:stu_id>",methods=["GET","POST"])
@login_required
def delete_stud(stu_id):
    if current_user.role != 'admin':
        flash('您没有权限删除学生记录')
        return redirect(url_for('main.dashboard'))
    stud = Student_Info.query.get(stu_id)
    db.session.delete(stud)
    db.session.commit() 
    flash('The record is deleted') 
    return redirect(url_for('main.dashboard'))