from flask_wtf import FlaskForm
from wtforms import DateTimeField, IntegerField, SelectField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.widgets import ListWidget, CheckboxInput
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
    start_date = DateTimeField('Дата начала работы',
        format='%d.%m.%Y',
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    submit = SubmitField('Добавить',
        render_kw={"class": "btn btn-primary"})

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class EventForm(FlaskForm):
    event_name = StringField('Название статьи',
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    text = TextAreaField('Текст статьи',
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    interval = IntegerField('Интервал отправки',
        validators=[DataRequired()],
        render_kw={"class": "form-control"})
    position_type = MultiCheckboxField('Позиции',
        choices=[],
        coerce=int)
    submit = SubmitField('Добавить',
        render_kw={"class": "btn btn-primary"})