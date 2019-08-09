from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from webapp.admin.form import PositionForm, UserForm
from webapp.model import db, Position_type, Role, User
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/administration')


@blueprint.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
    title = 'Пользователи'
    role = [(r.id, r.name) for r in Role.query.all()]
    form = UserForm()
    form.role.choices = role
    users_list = User.query.all()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        role = form.role.data
        username = form.username.data
        password = form.password.data
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        role=role,
                        username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь {} добавлен'.format(username))
        return redirect(url_for('admin.users'))

    return render_template('admin/user.html', title=title, form=form, users_list=users_list)


@blueprint.route('/position', methods=['GET', 'POST'])
@admin_required
def positions():
    title = 'Позиции'
    form = PositionForm()
    position_list = Position_type.query.all()
    print(position_list)

    if form.validate_on_submit():
        new_position = Position_type(position_name=form.position_name.data)
        db.session.add(new_position)
        db.session.commit()
        flash('Позиция добавлена')
        return redirect(url_for('admin.positions'))

    return render_template('admin/position.html', title=title, form=form, position_list=position_list)
