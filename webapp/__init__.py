from flask import Flask, render_template, url_for, redirect, request, flash
from webapp.form import UserForm, EventForm
from webapp.model import db, Event, User, Position_type

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Главная страница'
        hello_text = 'Hello, world!'
        return render_template('index.html', title=title, hello_text=hello_text)

    @app.route('/event', methods=['GET', 'POST'])
    def event():
        title = 'Статьи'
        positions = [(p.id, p.position_name) for p in Position_type.query.all()]
        event_form = EventForm(request.form)
        event_form.position_type.choices = positions
        events_list = Event.query.all()

        if event_form.validate_on_submit():
            event_name = event_form.event_name.data
            text = event_form.text.data
            interval = event_form.interval.data
            positions = Position_type.query.filter(Position_type.id.in_(event_form.position_type.data)).all()
            new_event = Event(event_name=event_name,
                              text=text,
                              interval=interval,
                              positions=positions)
            db.session.add(new_event)
            db.session.commit()
            flash('Статья успешно добавлена.')
            return redirect(url_for('event'))
 
        return render_template('event.html', title=title, form=event_form, events_list=events_list)

    @app.route('/users', methods=['GET', 'POST'])
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
            db.session.add(new_user)
            db.session.commit()
            flash('Пользователь успешно добавлен.')
            return redirect(url_for('users'))

        return render_template('users.html', title=title, form=user_form, users_list=users_list)

    return app