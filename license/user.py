import requests,json
url = "https://hcn1-license-default-rtdb.firebaseio.com/{0}/{1}/plans.json"

class User:
    def __init__(self,username:str,program:str):
        self.program = program
        self.username = username
        self.permessions = {
            "SERVER":False,
            "ALL-TOOLS":False,
            "LIMITE":0,
            "THREADS":5,
            "USED":0
        }

    def get_alias(self,code):
        url = "https://hcn1.net/api/v1/shortner"
        data = {"code":code}
        return json.loads(requests.get(url,json=data).text)["exist"]
    
    def get_plans(self):
        self.permessions["SERVER"] = True
        self.permessions["ALL-TOOLS"] = True
        self.permessions["LIMIT"] = self.__get_limit_attr()[self.__get_type_attr()]
        self.permessions["THREADS"] = 32
        self.permessions["USED"]  = self.__get_used_attr()

    def check_limit(self):
        return self.permessions.get("USED") == self.permessions.get("LIMIT")

    def __get_used_attr(self) -> str:
        return json.loads(requests.get(url.format(self.program,self.username)))["used"]
    
    def __get_type_attr(self) -> str:
        return json.loads(requests.get(url.format(self.program,self.username)))["type"]
    
    def __get_limit_attr(self) -> dict:
        return json.loads(requests.get(url.format(self.program,self.username)))["limit"]