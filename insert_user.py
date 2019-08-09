from webapp import create_app
from webapp.model import db, User, Role

app = create_app()
with app.app_context():
    new_role = Role(name='user')
    new_admin = User(first_name='User',
                     last_name='Slack-bot User',
                     username='user',
                     role_type=new_role)
    new_admin.set_password('user')

    db.session.add_all([new_role, new_admin])
    db.session.commit()
