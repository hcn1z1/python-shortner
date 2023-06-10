import json,time,flask
from func.database import Connecter

class BannedStand:
    def __init__(self) -> None:
        self.botHeaders = [instance for data in json.loads(open("database/crawler-user-agents.json", "r").read()) for instance in data["instances"]]
        self.connection:Connecter = None
        self.bannedIpAddrs:list = None
        self.suspendedIpAddrs:list[tuple] = None

    def setConnection(self,conn:Connecter):
        self.connection:Connecter = conn
        self.setBannedIps()
        self.setSuspendedIps()
    def setBannedIps(self):
        self.bannedIpAddrs = list(self.connection.execute("SELECT * FROM BANNED").fetchall())
    
    def setSuspendedIps(self):
        self.suspendedIpAddrs = list(self.connection.execute("SELECT * FROM SUSP").fetchall())

    def addBannedIp(self,ipAddr):
        self.bannedIpAddrs.append(ipAddr)
        self.connection.execute(f"INSERT INTO BANNED VALUES ('{ipAddr}')")
    
    def addSuspendedIp(self,ipAddr,suspension):
        self.bannedIpAddrs.append((ipAddr,suspension))
        self.connection.execute(f"INSERT INTO BANNED VALUES ('{ipAddr}')")

    def checkBannedIp(self,ipAddr):
        if any(ipAddr in ip[0] for ip in self.bannedIpAddrs):
            return False
        else:
            return True

    def checkSuspendedIp(self,ipAddr):
        if any(ipAddr in ip[0] and ip[1] + 300 >=time.time() for ip in self.suspendedIpAddrs) :
            return False
        else :
            try:self.connection.execute(f"DELETE FROM SUSP WHERE ipAddr='{ipAddr}'") # remove from suspension
            except:pass
            [self.suspendedIpAddrs.pop(item) for item in self.suspendedIpAddrs if item[0] == ipAddr]
            return True
        
    def checkUserAgent(self,userAgent:str):
        if userAgent in self.botHeaders : return False
        else : return True
    
    def checkRequest(self,request:flask.request):
        javascriptSupport = request.form.get('javascript_supported') == 'true' 
        bannedIp = self.checkBannedIp(request.remote_addr)
        suspendedIp = self.checkSuspendedIp(request.remote_addr)
        userAgentDetection = self.checkUserAgent(request.headers.get('User-Agent'))
        if not userAgentDetection : self.addBannedIp(request.remote_addr)
        return javascriptSupport and bannedIp and suspendedIp and userAgentDetection
