import requests
import os,json

class AntibotApis:
    def initializeAll(self,ipAddr) -> bool:
        hackertarget = self.hackerTarget(ipAddr)
        stopforumespam = self.stopForumeSpam(ipAddr)
        proxy = self.proxyCheck(ipAddr)
        return hackertarget and stopforumespam and proxy
    
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