from flask import render_template, redirect, url_for, flash, request
from . import auth  # 导入当前蓝图实例
from .. import db    # 导入 app 实例
from ..models import User
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember'))
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', error='用户名或密码错误')

@auth.route('/signup', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('main.home'))