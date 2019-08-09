from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class UserForm(FlaskForm):
    first_name = StringField('Имя',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    role = SelectField('Ролья пользователя',
                       choices=[],
                       coerce=int,
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


class PositionForm(FlaskForm):
    position_name = StringField('Наименование позиции',
                                validators=[DataRequired()],
                                render_kw={"class": "form-control"})
    submit = SubmitField('Сохранить',
                         render_kw={"class": "btn btn-primary"})
