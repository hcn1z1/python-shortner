import time,json,datetime
from flask import request

class Link:
    def __init__(self) -> None:
        self.folderPath:str = "database/links/"

    def initializeLink(self,shortner):
        name = f"{self.folderPath}{shortner}.json"
        informations:dict = {}
        informations["code"]:str = shortner
        informations["links"]:list = []
        informations["creation-time"]:str = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        informations["actions"]:list[dict] = []
        json.dump(informations,open(name,"w+"),indent=4)

    def pushLink(self,link:str,shortner:str):
        name = f"{self.folderPath}{shortner}.json"
        informations:dict = json.load(open(name,"r"))
        if link not in informations["links"] : informations["links"].append(link)
        json.dump(informations,open(name,"w+"),indent=4)

    def pushAction(self,shortner:str,request:request,is_bot:bool):
        name = f"{self.folderPath}{shortner}.json"
        informations:dict = json.load(open(name,"r"))
        click:dict = {}
        click["code"]:str = shortner
        click["ip"] = request.remote_addr
        click["user-agent"] = request.headers.get('User-Agent')
        click["time"]:str = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        click["bot"] = is_bot
        click["click-id"] = len([ip["ip"] in informations["actions"] for ip in informations["actions"] if ip["ip"] == click["ip"]])
        informations["actions"].insert(0,click)
        json.dump(informations,open(name,"w+"),indent=4)

    def getLink(self,shortner):
        name = f"{self.folderPath}{shortner}.json"
        informations:dict = json.load(open(name,"r"))
        return informations["links"]