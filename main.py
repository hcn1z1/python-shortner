from flask import Flask,render_template,request,redirect
from func import database
from antibot.bot import BannedStand
import json

app = Flask(__name__)
db = database.connecter("database/database.db")
antibot = BannedStand()
antibot.setConnection(db)

@app.route("/<identificator>",methods=["GET","POST"])
def redirecter(identificator):
    if request.method =="POST":
        data = json.loads(request.get_data().decode("utf-8"))
        try:
            if data["javascript"] == True and antibot.checkSuspendedIp(): pass
        except:
            pass
    return redirect("https://facebook.com")

@app.route("/api/shortner",methods=["POST"])
def generator():
    pass
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=8100, ssl_context='adhoc')