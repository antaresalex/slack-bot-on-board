from webapp import db, create_app

db.drop_all(app=create_app())
db.create_all(app=create_app())
