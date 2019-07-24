from pathlib import Path

basedir = Path(__file__).resolve().parent.parent

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir.joinpath('bot_db.sqlite').as_posix()
SECRET_KEY = 'sEcRe7K3y'

SQLALCHEMY_TRACK_MODIFICATION = False
