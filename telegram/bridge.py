from telebot import TeleBot,types
from dotenv import load_dotenv
import os
import requests
from license.license import License

load_dotenv()

key = License("Link Shortner")

bot:TeleBot = TeleBot(os.getenv("telegram"))

def communicate(chatid,information:str):
    bot.send_message(chatid,information)

users = {}  # Store user login status

@bot.message_handler(commands=['login'])
def start(message):
    chat_id = message.chat.id
    if chat_id in users and users[chat_id]["logged_in"] is True:
        bot.send_message(chat_id, "You are already logged in!")
    else:
        users[chat_id] = {'logged_in': False, 'username': '', 'password': ''}
        bot.send_message(chat_id, "Please enter your username:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in users and not users[chat_id]['logged_in']:
        if not users[chat_id]['username']:
            users[chat_id]['username'] = message.text
            bot.send_message(chat_id, "Please enter your password:")
        elif not users[chat_id]['password']:
            users[chat_id]['password'] = message.text
            # Perform login verification here
            if key.check_license(users[chat_id]['username'], users[chat_id]['password']):
                users[chat_id]['logged_in'] = True
                bot.send_message(chat_id, "Login successful! You are now logged in.")
            else:
                bot.send_message(chat_id, "Invalid username or password. Please try again.")
                users[chat_id] = {'logged_in': False, 'username': '', 'password': ''}
    elif chat_id in users and users[chat_id]['logged_in']:
        handle_links(message)
    else:
        bot.send_message(chat_id, "Please login first.")


def handle_links(message):
    api = "https://127.0.0.1:8100/api/shortner"
    url = message.text
    print("here")
    if "vs-s" in url:
        try:
            vvath,newLink = url.split(";")
            data = {"url":newLink,"shortner":vvath[len(vvath)-6:],"telegram":message.chat.id}
            response = requests.post(api,json=data,verify=False)
            if response.status_code == 500 : bot.send_message(message.chat.id,"not a valide link !\nexample of valide link : https://example.com")
            else : bot.send_message(message.chat.id,"https://vs-s.link/"+response.text)
        except:
            bot.send_message(message.chat.id,"Bad Link")
    else:
        response = requests.post(api,json={"url":url,"telegram":message.chat.id},verify=False)
        if response.status_code == 500 : bot.send_message(message.chat.id,"not a valide link !\nexample of valide link : https://example.com")
        else : bot.send_message(message.chat.id,"https://vs-s.link/"+response.text)