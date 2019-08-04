from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from webapp.model import User
from webapp.user.form import LoginForm

blueprint = Blueprint('user', __name__)


@blueprint.route('/login')
def login():
    text = 'Войдите'
    login_form = LoginForm()
    return render_template('user/login.html', text=text, form=login_form)


@blueprint.route('/process-login', methods=["POST"])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.chek_password(form.password.data):
            login_user(user)
            flash('Успешная авторизация')
            return redirect(url_for('index'))


@blueprint.route('/logout')
def loguot():
    logout_user()

    return redirect(url_for('user.login'))
