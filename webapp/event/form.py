from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, StringField, \
    SubmitField, TextAreaField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import DataRequired, InputRequired


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(html_tag='ol', prefix_label=False)
    option_widget = CheckboxInput()


class EventForm(FlaskForm):
    event_name = StringField('Название статьи',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    text = TextAreaField('Текст статьи',
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    interval = IntegerField('Интервал отправки',
                            validators=[InputRequired()],
                            render_kw={"class": "form-control"})
    position_type = MultiCheckboxField('Позиции',
                                       choices=[],
                                       coerce=int)
    submit = SubmitField('Добавить',
                         render_kw={"class": "btn btn-primary"})
