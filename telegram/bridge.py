from telebot import TeleBot,types
from dotenv import load_dotenv
import os
import requests
from license.license import License
from license.user import User

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
        users[chat_id] = {'logged_in': False, 'username': '', 'password': '','alias':False}
        bot.send_message(chat_id, "Please enter your username:")

@bot.message_handler(commands=["alias"])
def alias_managing(message):
    if message.chat.id in users and users[message.chat.id]["logged_in"] is True:
        try: alias,url = message.text.split("/alias ")[1].split(" ")
        except: alias,url = "",""
        if alias == "" or url == "": bot.send_message(message.chat.id,"Invalide format ! must be /alias alias https://example.com");return None
        user = User(users[message.chat.id]['username'],'Link Shortner')
        user.get_plans()
        if user.check_limit() or True:
            if user.get_alias(code=alias):
                bot.send_message(message.chat.id,"This alias is already assigned by another account ! ")
            else:
                message.text = url
                handle_links(message,alias)
        else: 
            bot.send_message("You reached your limit ! Please upgrade or contact @tools_designer",message.chat.id)
    else : 
        bot.send_message(message.chat.id,"Please login first /login.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to your bot! Use /add link <url> or /add to <link> new <new_url> to add links.")

@bot.message_handler(commands=['add'])
def add_link(message):
    args = message.text.split()
    
    if len(args) == 3 and args[1] == 'link':
        link = args[2]
        # Save the 'link' somewhere or perform desired action.
        bot.reply_to(message, f"Added link: {link}")
    
    elif len(args) == 5 and args[1] == 'to' and args[3] == 'new':
        original_link = args[2]
        new_link = args[4]
        code = original_link.split("/")[len(original_link.split("/"))-1]
        message.text = new_link
        handle_links(message,code)
        bot.reply_to(message, f"Added new link '{new_link}' to '{original_link}'")

    else:
        bot.reply_to(message, "Invalid command format. Use /add to <link> new <new_url>.")

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
                users[chat_id] = {'logged_in': False, 'username': '', 'password': '','alias':False}
    elif chat_id in users and users[chat_id]['logged_in']:
        handle_links(message)
    else:
        bot.send_message(chat_id, "Please login first.")


def handle_links(message,alias = False):
    api = "https://vs-s.link/api/shortner"
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

        if bool(alias) == False : response = requests.post(api,json={"url":url,"telegram":message.chat.id},verify=False)
        else : response = requests.post(api,json={"url":url,"telegram":message.chat.id,"shortner":alias},verify=False)
        if response.status_code == 500 : bot.send_message(message.chat.id,"not a valide link !\nexample of valide link : https://example.com")
        else : bot.send_message(message.chat.id,"https://vs-s.link/"+response.text)