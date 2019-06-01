import os
import json
import slack

def bot_token():
    with open('bot_slack_settings.json', 'r') as f_bot_token:
        bot_token = json.loads(f_bot_token.read())["bot_token"]
        return bot_token

def proxy_login_data():
    with open('bot_slack_settings.json', 'r') as f_proxy_login:
        proxy_login = json.loads(f_proxy_login.read())["bot_proxy"]["http"]
        return proxy_login

def hello_bot():
    client = slack.WebClient(
        token=bot_token(),
        proxy=proxy_login_data())
    response = client.chat_postMessage(
        channel='UJVLRJ9P0',
        text='Yo!')

if __name__ == '__main__':
    hello_bot()

#print(client.chat_postMessage.__doc__)