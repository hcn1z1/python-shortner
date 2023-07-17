import time,json,datetime
from flask import request
from telegram.bridge import communicate
import requests

class Link:
   
    def __init__(self) -> None:
        self.url:str = "https://hcn1.net/api/v1/shortner"
        self.headers = {
            "Content-Type":"application/json"
        }
    def initializeLink(self,shortner,telegram = -1):
        print("at least you are here?")
        url = f"{self.url}"
        informations:dict = {}
        informations["code"]:str = shortner
        informations["links"]:list = []
        informations["telegram"]:list = str(telegram)
        informations["creation-time"]:str = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        informations["actions"]:list[dict] = []
        print(requests.post(url,json = informations).text)

    def pushLink(self,link:str,shortner:str):
        url = f"{self.url}/{shortner}"
        print(requests.post(url,json={"link":link}).text)

    def pushAction(self,shortner:str,request:request,redirection,is_bot:bool):
        print("pushing actions")
        url = f"{self.url}/{shortner}"
        click:dict = {}
        click["code"]:str = shortner
        click["url"]:str = redirection
        click["ip"] = request.remote_addr
        click["user-agent"] = request.headers.get('User-Agent')
        click["time"]:str = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
        click["bot"] = is_bot
        print(requests.get(url,json= {"id":-1}).text)
        click["click-id"] = json.loads(requests.get(url,json= {"id":-1}).text)["length"]
        telegram = json.loads(requests.post(url,json={"telegram":True}).text)["telegram"]
        print(requests.post(url,json= click).text)
        self.sendTelegram(click,telegram)

    def getAction(self,shortner:str,click_id = -1):
        url = f"{self.url}/shortner"
        data = {"id":click_id}
        informations:dict = json.load(open(url,"r"))
        clicks:list = informations["actions"]
        if click_id != -1: return json.dumps(clicks[len(clicks) - click_id -1])
        else: return json.dumps(clicks[0])

    def getLink(self,shortner):
        url = f"{self.url}/{shortner}"
        informations:dict = json.loads(requests.get(url,headers=self.headers).text)
        return informations
    
    def sendTelegram(self,data:dict,telegram):
        if telegram != "-1": communicate(telegram,'\n'.join([f'{key} : {value}' for key, value in data.items()]))