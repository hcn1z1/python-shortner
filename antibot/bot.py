import json,time
import sqlite3

class BannedStand:
    def __init__(self) -> None:
        self.bot_headers = json.loads(open("database/crawler-user-agents.json","r").read())
        self.connection = None
        self.bannedIpAddrs:list = None
        self.suspendedIpAddrs:list[tuple] = None
    
    def setConnection(self,conn:sqlite3.Connection):
        self.connection:sqlite3.Connection = conn
        self.setBannedIps()
        self.setSuspendedIps()
    def setBannedIps(self):
        self.bannedIpAddrs = list(self.connection.execute("SELECT * FROM BANNED"))
    
    def setSuspendedIps(self):
        self.suspendedIpAddrs = list(self.connection.execute("SELECT * FROM SUSPENDED"))

    def addBannedIp(self,ipAddr):
        self.bannedIpAddrs.append(ipAddr)
        self.connection.execute(f"INSERT INTO BANNED VALUES ('{ipAddr}')")
    
    def addSuspendedIp(self,ipAddr,suspension):
        self.bannedIpAddrs.append((ipAddr,suspension))
        self.connection.execute(f"INSERT INTO BANNED VALUES ('{ipAddr}')")

    def checkSuspendedIp(self,ipAddr):
        if any(ipAddr in ip[0] and ip[1] + 300 <time.time() for ip in self.suspendedIpAddrs):
            pass
        else:
            self.connection.execute(f"DELETE FROM SUSPENDED WHERE ipAddr='{ipAddr}'") # remove from suspension
            [self.suspendedIpAddrs.pop(item) for item in self.suspendedIpAddrs if item[0] == ipAddr]

