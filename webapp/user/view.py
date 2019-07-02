from datetime import datetime, timedelta
from flask import Blueprint, render_template, url_for, redirect, request, flash

from webapp.user.form import UserForm
from webapp.model import db, Event, User, Position_type, Schedule

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/', methods=['GET', 'POST'])
def users():
    title = 'Пользователи'
    positions = [(p.id, p.position_name) for p in Position_type.query.all()]
    user_form = UserForm(request.form)
    user_form.position_type.choices = positions
    users_list = User.query.all()

    if user_form.validate_on_submit():
        first_name = user_form.first_name.data
        last_name = user_form.last_name.data
        slack_id = user_form.slack_id.data
        position_type = user_form.position_type.data
        start_date = user_form.start_date.data
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        slack_id=slack_id,
                        start_date=start_date,
                        position_type=position_type)
        schedule_to_insert = [new_user]
        events = Event.query.filter(Event.positions.any(
            id=user_form.position_type.data)).all()

        for event in events:
            day_now = datetime.now().date()
            interval = timedelta(days=event.interval)
            delivery_date = start_date + interval

            if delivery_date < day_now:
                continue

            schedule_to_insert.append(Schedule(user=new_user,
                                               event_id=event.id,
                                               delivery_date=delivery_date))
        db.session.add_all(schedule_to_insert)
        db.session.commit()
        flash('Пользователь успешно добавлен.')
        return redirect(url_for('user.users'))

    return render_template('user/users.html',
                           title=title,
                           form=user_form,
                           users_list=users_list)


@blueprint.route('/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    title = 'Пользователь: {firstname} {lastname}'.format(
        firstname=user.first_name, lastname=user.last_name)
    form = UserForm(obj=user)
    form.position_type.choices = [
        (user.position.id, user.position.position_name)]

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.slack_id = form.slack_id.data
        db.session.commit()
        flash('Пользователь {firstname} {lastname} успешно обнавлен.'.format(
            firstname=user.first_name, lastname=user.last_name))
        return redirect(url_for('user.users'))

    return render_template('user/edit_user.html',
                           title=title,
                           user=user,
                           form=form)


@blueprint.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return 'Пользователь успешно удален!'
    else:
        return 'Error'
