from webapp import create_app
from webapp.model import db, User, Role

app = create_app()
with app.app_context():
    new_role = Role(name='admin')
    new_admin = User(first_name='Admin',
                     last_name='Slack-bot',
                     username='admin',
                     role_type=new_role)
    new_admin.set_password('admin')

    db.session.add_all([new_role, new_admin])
    db.session.commit()
