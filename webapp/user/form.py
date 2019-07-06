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
    start_date = DateField('Дата начала работы xx.xx.xxxx',
                           format='%d.%m.%Y',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    submit = SubmitField('Добавить',
                         render_kw={"class": "btn btn-primary"})
