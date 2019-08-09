from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Войти',
                         render_kw={"class": "btn btn-primary"})


class EditUserForm(FlaskForm):
    first_name = StringField('Имя',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=3, message='Длинна пароля должна быть более 3 символов'),
                                         EqualTo('confirm', message='Пароли не совпадают')],
                             render_kw={"class": "form-control"})
    confirm = PasswordField('Повторите пароль',
                            render_kw={"class": "form-control"})
    submit = SubmitField('Сохранить',
                         render_kw={"class": "btn btn-primary"})
