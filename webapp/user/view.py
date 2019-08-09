from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from webapp.model import db, User
from webapp.user.form import LoginForm, EditUserForm

blueprint = Blueprint('user', __name__)


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    text = 'Войдите'
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Добро пожаловать, {}'.format(user.first_name))
            return redirect(url_for('index'))
    flash('Не правильное имя или пароль')
    return render_template('user/login.html', text=text, form=form)


@blueprint.route('/logout')
def loguot():
    logout_user()

    return redirect(url_for('user.login'))


@blueprint.route('/profile/<int:user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user == current_user:
        flash('Доступ запрещен')
        return redirect(url_for('index'))
    title = '{} {}'.format(user.first_name, user.last_name)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.commit()
        flash('Данные сохранены!')
        return redirect(url_for('user.edit_user', user_id=user_id))

    return render_template('user/profile.html', title=title, form=form)
