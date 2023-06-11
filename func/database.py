import sqlite3
from .generater import generator

class Connecter:
    def __init__(self,path):
        self.conn = sqlite3.connect(path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.sqlReq = "INSERT INTO URLS VALUES ('{0}','{1}','')"

    def addUser(self,user,identifictor):
        try:self.cursor.execute(self.sqlReq.format(user,identifictor))
        except Exception as e:print(e);return None
        self.conn.commit()
        return identifictor
    
    def getUser(self,identificator):
        self.conn.commit()
        self.conn.close()
        self.__init__("database/database.db")
        print("reinitializing my database")
        try:
            url = self.cursor.execute(f"SELECT user FROM URLS WHERE identificator='{identificator}'").fetchall()[0][0]
            if not bool(url):
                raise Exception
            return url
        except Exception as e:return "/error"

    def generate(self,url):
        return generator()
    
    def execute(self,query):
        return self.cursor.execute(query)