import requests
import os,json
import dotenv
import socket
from func.customthread import Worker

dotenv.load_dotenv()

class AntibotApis:
    def initializeAll(self,ipAddr) -> bool:
        hackertarget = Worker(target = self.hackerTarget,args = (ipAddr,))
        stopforumespam = Worker(target=self.stopForumeSpam,args=(ipAddr,))
        proxy = Worker(target = self.proxyCheck, args = (ipAddr,))
        reverse_dns = Worker(target =self.resolveDns,args=(ipAddr,))

        # running on parallel
        hackertarget.start()
        stopforumespam.start()
        proxy.start()
        reverse_dns.start()

        reverse_dns.join()
        proxy.join()
        stopforumespam.join()
        hackertarget.join()
        
        return hackertarget.value and stopforumespam.value and proxy.value and reverse_dns.value
    
    def googleSafeBrowsing(self,url:str):
        googleApi = os.getenv("google")
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={googleApi}"
        payload = {
            "client": {
                "clientId": "yourcompany",
                "clientVersion": "1.5.2"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        response = requests.post(api_url, json=payload)
        if "matches" in response.text: return False
        else : return True

    def hackerTarget(self,ipAddr:str):
        htApi = f"https://api.hackertarget.com/reverseiplookup/?q={ipAddr}"
        response = requests.get(htApi)
        if "google" in response.text : return False
        else : return True

    def proxyCheck(self,ipAddr):
        url = f"https://proxycheck.io/v2/{ipAddr}?vpn=1&asn=1"
        response = requests.get(url)
        try:
            if json.loads(response.text)[ipAddr]["currency"]["proxy"] == "yes" : return False
            else : raise Exception
        except : return True

    def stopForumeSpam(self,ipAddr):
        url = f'http://api.stopforumspam.org/api?ip={ipAddr}'
        response = requests.get(url)
        if "yes" in response : return False
        else : return True

    def resolveDns(self,ipAddr):
        reversed_dns = socket.getnameinfo((ipAddr,0),0)[0]
        if "google" in reversed_dns : return False
        else: return True
        