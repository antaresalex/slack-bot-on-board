from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from webapp.model import db, User
from webapp.admin.view import blueprint as admin_blueprint
from webapp.employee.view import blueprint as employee_blueprint
from webapp.event.view import blueprint as event_blueprint
from webapp.user.view import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(event_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_manager(user_id):
        return User.query.get(user_id)

    @app.before_request
    def before_request():
        if current_user.is_anonymous and (request.endpoint != 'user.login'):
            return redirect(url_for('user.login'))

    @app.route('/')
    def index():
        title = 'Главная страница'
        hello_text = 'Hello, world!'
        return render_template('index.html',
                               title=title,
                               hello_text=hello_text)

    return app
