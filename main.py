from flask import Flask,render_template,request,redirect
from func.core import Core
from antibot.bot import BannedStand
from telegram.bridge import bot
import threading
from waitress import serve
import json

app = Flask(__name__)
db = Core("database/database.db")
antibot = BannedStand()
antibot.setConnection(db)

@app.route("/<identificator>",methods=["GET","POST"])
def redirecter(identificator):
    if request.method =="POST":
        try:
            print("to redirect",db.redirectLink(identificator))
            if db.redirectLink(identificator) == "/error":
                return redirect(db.redirectLink(identificator))
            if antibot.checkRequest(request):
                request.remote_addr = "imma change it"
                db.pushAction(identificator,request,db.redirectLink(identificator),False)
                return redirect(db.redirectLink(identificator))
            else:
                db.pushAction(identificator,request,True)
                return "<title>No redirection</title>"
                
        except Exception as e:
            print("Error !" , e)
            pass
    print("Get remote address " ,request.remote_addr)
    print(str(request))
    return render_template("index.html")

@app.route("/api/shortner",methods=["POST"])
def shortner():
    data = json.loads(request.get_data().decode("utf-8"))
    url = data["url"]
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


if __name__ == "__main__":
    threading.Thread(target = bot.polling).start()
    serve(app, host="0.0.0.0", port=8100)
    app.run(host="0.0.0.0", port=8100,debug=True,ssl_context='adhoc')