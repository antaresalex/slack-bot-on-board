from flask import Flask, render_template

from webapp.model import db
from webapp.user.view import blueprint as user_blueprint
from webapp.event.view import blueprint as event_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(event_blueprint)

    @app.route('/')
    def index():
        title = 'Главная страница'
        hello_text = 'Hello, world!'
        return render_template('index.html',
                               title=title,
                               hello_text=hello_text)

    return app
