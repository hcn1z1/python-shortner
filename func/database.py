import sqlite3
import generater

class connecter:
    def __init__(self,path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.sqlReq = "INSERT INTO URLS VALUES ('{0}','{1}')"

    def addUrl(self,url,identifictor):
        try:self.cursor.execute(self.sqlReq.format(url,identifictor))
        except:return None
        return identifictor
    
    def getURL(self,identificator):
        try:return self.cursor.execute(f"SELECT url FROM URLS WHERE identificator={identificator}")[0]
        except:return None

    def generate(self,url):
        i = 0
        while i<5:
            i=+1
            try:
                identifictor=generater.generator()
                return self.addUrl(url=url,identifictor=identifictor)
            except Exception as e:
                error = e
                print("Error :", e.__traceback__)
        return str(error)