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
# Вторая функция в цикле отправляет сообщения и отмечает в базе статус отправлено

def get_from_database():
    schedule_from_base = (db.session.query(Schedule, User, Event)
    .join(User)
    .join(Event)
    .filter(Schedule.delivery_status == None)
    .filter(Schedule.delivery_date <= datetime.today())
    .all())
    return schedule_from_base

#список с кортежем// в цикле итерирусь по списку для sch, user, event
def send_message():
    schedule_from_base = get_from_database()
    for schedule, user, event in schedule_from_base:
        client = slack.WebClient(
            token=bot_token(),
            proxy=proxy_login_data())
        response = client.chat_postMessage(
            channel=user.slack_id,
            text=event.text)
    #отметить статус Отправлено в БД в расписании после каждой отправки


# def hello_bot():
#     list_ID_Sch = database()
#     for user_id, message in list_ID_Sch:
#         client = slack.WebClient(
#             token=bot_token(),
#             proxy=proxy_login_data())
#         response = client.chat_postMessage(
#             channel=user_id,
#             text=message)

    
    # with open('database_test.json', 'r') as f_ID_Sch:
    #     list_ID_Sch = []
    #     dict_ID_Sch = json.loads(f_ID_Sch.read())
    #     for ID_Sch in dict_ID_Sch.values():
    #         user_ID = ID_Sch["User ID"]
    #         user_message = ID_Sch["Message"]
    #         list_ID_Sch_user = []
    #         list_ID_Sch_user.append(user_ID)
    #         list_ID_Sch_user.append(user_message)
    #         list_ID_Sch.append(list_ID_Sch_user)
    #     print(list_ID_Sch)
    #     return list_ID_Sch

    #     app = create_app()
    #     with app.app_context():
    #         get_user_db()


#def database():
#    with open('database_test.json', 'r') as f_ID_Sch:
#        list_ID_Sch = []
#        dict_ID_Sch = json.loads(f_ID_Sch.read())
#        for ID_Sch in dict_ID_Sch.values():
#            user_ID = ID_Sch["User ID"]
#            user_message = ID_Sch["Message"]
#            list_ID_Sch_user = []
#            list_ID_Sch_user.append(user_ID)
#            list_ID_Sch_user.append(user_message)
#            list_ID_Sch.append(list_ID_Sch_user)
#        print(list_ID_Sch)
#        return list_ID_Sch

# def message():
#     with open('database_test.json', 'r') as f_bot_message:
#         bot_message = json.loads(f_bot_message.read())["bot_message"]
#         return bot_message

# def get_user_ID():
#     with open('database_test.json', 'r') as f_user_ID:
#         user_ID = json.loads(f_user_ID.read())["ID Sch 1"]["User ID"]
#         return user_ID

# def hello_bot():
#     list_ID_Sch = database()
#     for user_id, message in list_ID_Sch:
#         client = slack.WebClient(
#             token=bot_token(),
#             proxy=proxy_login_data())
#         response = client.chat_postMessage(
#             channel=user_id,
#             text=message)

# def bot_job():
#     print("I'm in bot_job...")
#     schedule.every().minute.do(hello_bot)
#     #schedule.every().day.at("11:00").do(hello_bot)

#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# if __name__ == '__main__':
#     bot_job()

app = create_app()
with app.app_context():
    send_message()


