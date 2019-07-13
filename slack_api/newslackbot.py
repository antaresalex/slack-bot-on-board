import json
import slack
import schedule
import time
from datetime import datetime
from webapp import create_app
from webapp.model import db, User, Event, Position_type, Schedule

def bot_token():
    with open('/Users/aleksandrakulikova/pythonproject/LP13/slack_api/bot_slack_settings.json', 'r') as f_bot_token:
        bot_token = json.loads(f_bot_token.read())["bot_token"]
        return bot_token

def proxy_login_data():
    with open('/Users/aleksandrakulikova/pythonproject/LP13/slack_api/bot_slack_settings.json', 'r') as f_proxy_login:
        proxy_login = json.loads(f_proxy_login.read())["bot_proxy"]["http"]
        return proxy_login

# Одна функция - джойн нескольких таблиц (все данные для отправки сегодня)
def get_from_database():
    schedule_from_base = (db.session.query(Schedule, User, Event)
    .join(User)
    .join(Event)
    .filter(Schedule.delivery_status == None)
    .filter(Schedule.delivery_date <= datetime.today())
    .all())
    return schedule_from_base

#Вторая функция в цикле отправляет сообщения и отмечает в базе статус отправлено
def send_message():
    schedule_from_base = get_from_database()
    for schedule, user, event in schedule_from_base:
        client = slack.WebClient(
            token=bot_token(),
            proxy=proxy_login_data())
        response = client.chat_postMessage(
            channel=user.slack_id,
            text=event.text)
        schedule.delivery_status='Отправлено'
        db.session.add(schedule)
    db.session.commit()

#проверка базы каждый день на наличие неотравленных материалов
def bot_job():
    print("I'm in bot_job...")
    schedule.every().monday.at("11:00").do(send_message)
    schedule.every().tuesday.at("11:00").do(send_message)
    schedule.every().wednesday.at("11:00").do(send_message)
    schedule.every().thursday.at("11:00").do(send_message)
    schedule.every().friday.at("11:00").do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        bot_job()


