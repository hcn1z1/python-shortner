import sqlite3


class Connecter:
    def __init__(self,path):
        self.conn = sqlite3.connect(path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.sqlReq = "INSERT INTO URLS VALUES ('{0}','{1}','')"

    def execute(self,query):
        return self.cursor.execute(query)