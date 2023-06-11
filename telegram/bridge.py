from telebot import TeleBot
from dotenv import load_dotenv
import os
import requests

load_dotenv()

bot:TeleBot = TeleBot(os.getenv("telegram"))

def communicate(chatid,information:str):
    bot.send_message(chatid,information)

@bot.message_handler()
def shortner(message):
    api = "https://vvath.com/api/shortner"
    url = message.text
    if "vvath" in url:
        try:
            vvath,newLink = url.split(";")
            data = {"url":newLink,"shortner":vvath[len(vvath)-6:],"telegram":message.chat.id}
            response = requests.post(api,json=data).text
            bot.send_message(message.chat.id,"https://vvath.com/"+response)
        except:
            bot.send_message(message.chat.id,"Bad Link")
    else:
        response = requests.post(api,json={"url":url,"telegram":message.chat.id}).text
        bot.send_message(message.chat.id,"https://vvath.com/"+response)

