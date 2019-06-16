from flask import Flask, render_template, url_for, redirect, request
from webapp.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Главная страница'
        hello_text = 'Hello, world!'
        return render_template('index.html', title=title, hello_text=hello_text)

    @app.route('/success/<what>')
    def success(what):
        return render_template('success.html', what=what)

    @app.route('/event', methods=['GET', 'POST'])
    def event():
        title = 'Статьи'
        if request.method == 'POST':
            return redirect(url_for('success', what='Cтатья'))
        return render_template('event.html', title=title)

    @app.route('/users', methods=['GET', 'POST'])
    def users():
        title = 'Пользователи'
        if request.method == 'POST':
            return redirect(url_for('success', what='Пользователь'))
        return render_template('users.html', title=title)

    return app