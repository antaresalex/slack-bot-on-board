import json
import slack
import schedule
import time

def bot_token():
    with open('bot_slack_settings.json', 'r') as f_bot_token:
        bot_token = json.loads(f_bot_token.read())["bot_token"]
        return bot_token

def proxy_login_data():
    with open('bot_slack_settings.json', 'r') as f_proxy_login:
        proxy_login = json.loads(f_proxy_login.read())["bot_proxy"]["http"]
        return proxy_login

def hello_bot():
    print("I am in hello bot")
    client = slack.WebClient(
        token=bot_token(),
        proxy=proxy_login_data())
    response = client.chat_postMessage(
        channel='#general',
        text='Yo!')

def bot_job():
    print("I'm working...")
    schedule.every().minute.do(hello_bot)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    bot_job()
    