from flask import Flask,render_template,request,redirect
from func.core import Core
from func.database import Connecter
from antibot.bot import BannedStand
from func.generater import valideUrl
from telegram.bridge import bot
import threading
from waitress import serve
import json
from func.customthread import Worker

app = Flask(__name__)
db = Core()
database = Connecter("database/database.db")
antibot = BannedStand()
antibot.setConnection(database)

try: threading.Thread(target = bot.polling).start()
except: pass


@app.route("/")
def main():
    return render_template("main.html")

@app.route("/<identificator>",methods=["GET","POST"])
def redirecter(identificator):
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    request.remote_addr = ip_address
    if request.method =="POST":
        try:
            print("to redirect",db.redirectLink(identificator))
            if db.redirectLink(identificator) == "/error":
                return redirect(db.redirectLink(identificator))
            if antibot.checkRequest(request):
                db.pushAction(identificator,request,db.redirectLink(identificator),False)
                return redirect(db.redirectLink(identificator))
            else:
                db.pushAction(identificator,request,"/error",True)
                return "<title>No redirection</title>"
                
        except Exception as e:
            print("Error !" , e)

    return render_template("index.html")

@app.route("/api/shortner",methods=["POST"])
def shortner():
    data = json.loads(request.get_data().decode("utf-8"))
    url = data["url"]
    if not valideUrl(url):
        return "{'message':'not a valide url !'}",500
    try: shortner = data["shortner"]
    except: shortner = None
    try: telegram = data["telegram"]
    except: telegram = -1
    return db.generate(url,shortner,telegram) # returning identificator

@app.route("/api/shortner/get_info",methods =["POST"])
def post_info():
    data = json.loads(request.get_data().decode("utf-8"))
    short_url = data["url"]
    try: click_id = int(data["id"])
    except: click_id = -1
    short_url = short_url.replace("/","")
    try: data = db.getAction(short_url[len(short_url.replace("/",""))-6:],click_id=click_id)
    except: data = "{'message':'bad request. please check your query','status':500}",500
    return data

@app.route("/api/shortner/get_info/<short>/<click_id>",methods =["GET"])
def get_info(short:str,click_id:str):
    short_url = short
    click_id = int(click_id)
    short_url = short_url.replace("/","")
    try: data = db.getAction(short_url[len(short_url.replace("/",""))-6:],click_id=click_id)
    except: data = "{'message':'bad request. please check your query','status':500}",500
    return data

@app.route("/error")
def notfound():
    return "Page not found"
