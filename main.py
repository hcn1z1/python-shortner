from flask import Flask,render_template,request,redirect
from func.core import Core
from antibot.bot import BannedStand
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
            if antibot.checkRequest(request):
                db.pushAction(identificator,request,False)
                return redirect(db.redirectLink(identificator))
            else:
                db.pushAction(identificator,request,True)
                return "<title>No redirection</title>"
                
        except Exception as e:
            print("Error !" , e)
            pass
    return render_template("index.html")

@app.route("/api/shortner",methods=["POST"])
def shortner():
    data = json.loads(request.get_data().decode("utf-8"))
    url = data["url"]
    try: shortner = data["shortner"]
    except: shortner = None
    return db.generate(url,shortner) # returning identificator

@app.route("/error")
def notfound():
    return "Page not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8100,debug= True)