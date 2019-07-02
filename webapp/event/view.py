from flask import Blueprint, render_template, url_for, redirect, flash

from webapp.event.form import EventForm
from webapp.model import db, Event, Position_type

blueprint = Blueprint('event', __name__, url_prefix='/events')


@blueprint.route('/', methods=['GET', 'POST'])
def events():
    title = 'Статьи'
    positions = [(p.id, p.position_name) for p in Position_type.query.all()]
    event_form = EventForm()
    event_form.position_type.choices = positions
    events_list = Event.query.all()

    if event_form.validate_on_submit():
        event_name = event_form.event_name.data
        text = event_form.text.data
        interval = event_form.interval.data
        positions = Position_type.query.filter(Position_type.id.in_(
            event_form.position_type.data)).all()

        new_event = Event(event_name=event_name,
                          text=text,
                          interval=interval,
                          positions=positions)
        db.session.add(new_event)
        db.session.commit()
        flash('Статья успешно добавлена.')
        return redirect(url_for('event.events'))

    return render_template('event/event.html',
                           title=title,
                           form=event_form,
                           events_list=events_list)


@blueprint.route('/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get(event_id)
    title = 'Статья: {}'.format(event.event_name)
    form = EventForm(obj=event)
    form.position_type.choices = [
        (p.id, p.position_name) for p in event.positions]

    if form.validate_on_submit():
        event.event_name = form.event_name.data
        event.text = form.text.data
        db.session.commit()
        flash('{} сохранена'.format(event.event_name))
        return redirect(url_for('event.events'))

    return render_template('event/edit_event.html',
                           title=title,
                           event=event,
                           form=form)
