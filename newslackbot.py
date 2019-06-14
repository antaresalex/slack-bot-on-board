import json
import slack
import schedule
import time
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scored_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://schedule.sqlite')

db_session = scored_session(sessionmaker(bing=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def bot_token():
    with open('bot_slack_settings.json', 'r') as f_bot_token:
        bot_token = json.loads(f_bot_token.read())["bot_token"]
        return bot_token

def proxy_login_data():
    with open('bot_slack_settings.json', 'r') as f_proxy_login:
        proxy_login = json.loads(f_proxy_login.read())["bot_proxy"]["http"]
        return proxy_login

def database():
    with open('database_test.json', 'r') as f_ID_Sch:
        list_ID_Sch = []
        dict_ID_Sch = json.loads(f_ID_Sch.read())
        for ID_Sch in dict_ID_Sch.values():
            user_ID = ID_Sch["User ID"]
            user_message = ID_Sch["Message"]
            list_ID_Sch_user = []
            list_ID_Sch_user.append(user_ID)
            list_ID_Sch_user.append(user_message)
            list_ID_Sch.append(list_ID_Sch_user)
        print(list_ID_Sch)
        return list_ID_Sch

# def message():
#     with open('database_test.json', 'r') as f_bot_message:
#         bot_message = json.loads(f_bot_message.read())["bot_message"]
#         return bot_message

# def get_user_ID():
#     with open('database_test.json', 'r') as f_user_ID:
#         user_ID = json.loads(f_user_ID.read())["ID Sch 1"]["User ID"]
#         return user_ID

def hello_bot():
    list_ID_Sch = database()
    for user_id, message in list_ID_Sch:
        client = slack.WebClient(
            token=bot_token(),
            proxy=proxy_login_data())
        response = client.chat_postMessage(
            channel=user_id,
            text=message)

def bot_job():
    print("I'm in bot_job...")
    schedule.every().minute.do(hello_bot)
    #schedule.every().day.at("11:00").do(hello_bot)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    bot_job()

