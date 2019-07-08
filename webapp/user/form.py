from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    first_name = StringField('Имя пользователя',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    last_name = StringField('Фамилия пользователя',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    slack_id = StringField('Идентификатор Slack',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    position_type = SelectField('Позиция',
                                choices=[],
                                coerce=int,
                                render_kw={"class": "form-control"})
    start_date = DateField('Дата начала работы',
                           format='%d.%m.%Y',
                           validators=[DataRequired(message='Введите дату в формате 31.12.2019')],
                           render_kw={"class": "form-control datepicker"})
    submit = SubmitField('Добавить',
                         render_kw={"class": "btn btn-primary"})
