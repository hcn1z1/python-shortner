from flask import Flask,render_template,request,redirect
from func.database import *
from antibot.bot import BannedStand
from waitress import serve
import json

app = Flask(__name__)
db = Connecter("database/database.db")
antibot = BannedStand()
antibot.setConnection(db)

@app.route("/<identificator>",methods=["GET","POST"])
def redirecter(identificator):
    if request.method =="POST":
        try:
            print(db.getURL(identificator))
            if antibot.checkRequest(request):
                return redirect(db.getURL(identificator))
            else:
                return "<title>No redirection</title>"
                
        except Exception as e:
            print("Error !" , e)
            pass
    return render_template("index.html")

@app.route("/api/shortner",methods=["POST"])
def shortner():
    url = json.loads(request.get_data().decode("utf-8"))["url"]
    return db.generate(url) # returning identificator

@app.route("/error")
def notfound():
    return "Page not found"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8100)