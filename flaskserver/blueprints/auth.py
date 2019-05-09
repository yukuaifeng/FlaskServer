from flask import render_template, flash, redirect, url_for, Blueprint, make_response, session
from flask_login import login_user, logout_user, login_required, current_user

from flaskserver.forms import LoginForm, RegisterForm
from flaskserver.models import User
from flaskserver.utils import redirect_back, generate_token, validate_token
from flaskserver.verify_code import get_verify_code
from flaskserver.extensions import db
from flaskserver.settings import Operations
from flaskserver.emails import send_confirm_email


from io import BytesIO

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('server.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        verify_code = form.verify_code.data
        if session.get('image').lower() != verify_code.lower():
            flash('Wrong verify code.')
            return render_template('auth/login.html', form=form)
        user = User.query.filter_by(username=username).first()
        if user:
            if username is not None and user.validate_password(password):
                login_user(user, remember)
                flash('Welcome Back.', 'info')
                return redirect_back()  #返回上一个页面
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()

@auth_bp.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('server.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        verify_code = form.verify_code.data
        if session.get('image').lower() != verify_code.lower():
            flash('Wrong verify code.')
            return render_template('auth/register.html', form=form)
        user = User(email=email, username=username)
        user.set_password(password)
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('已发送确认邮件到您的注册邮箱，请您注意查收', 'info')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('server.index'))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash('用户已确认！', 'success')
        return redirect(url_for('server.index'))
    else:
        flash('无效过着过期的Token。', 'danger')
        redirect(url_for('.resend_confirm_email'))

@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash('重新发送了确认邮件，请注意查收！.', 'info')
    return redirect(url_for('server.index'))

