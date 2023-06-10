import sqlite3
from .generater import generator

class Connecter:
    def __init__(self,path):
        self.conn = sqlite3.connect(path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.sqlReq = "INSERT INTO URLS VALUES ('{0}','{1}')"

    def addUrl(self,url,identifictor):
        try:self.cursor.execute(self.sqlReq.format(url,identifictor))
        except Exception as e:return None
        self.conn.commit()
        return identifictor
    
    def getURL(self,identificator):
        self.conn.commit()
        self.conn.close()
        self.__init__("database/database.db")
        print("reinitializing my database")
        try:
            url = self.cursor.execute(f"SELECT url FROM URLS WHERE identificator='{identificator}'").fetchall()[0][0]
            if not bool(url):
                raise Exception
            return url
        except Exception as e:return "/error"

    def generate(self,url):
        i = 0
        while i<5:
            i=+1
            try:
                identifictor= generator()
                text =  self.addUrl(url=url,identifictor=identifictor)
                print(text)
                if bool(text) == None:
                    raise Exception
                return text
            except Exception as e:
                error = e
                print("Error :", e.__traceback__)
        return "/error"
    
    def execute(self,query):
        return self.cursor.execute(query)