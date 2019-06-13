from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Главная страница'
    hello_text = 'Hello, world!'
    return render_template('index.html', title=title, hello_text=hello_text)

@app.route('/success')
def success():
    title = 'Пользователь добавлен'
    return render_template('success.html', title=title)

@app.route('/users', methods=['GET', 'POST'])
def users():
    title = 'Пользователи'
    if request.method == 'POST':
        return redirect(url_for('success'))
    return render_template('users.html', title=title)

if __name__ == "__main__":
    app.run(debug=True)