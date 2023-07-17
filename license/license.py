from threading import Timer
import requests,multiprocessing
import uuid,json,os
import bcrypt

database_url = "https://hcn1-license-default-rtdb.firebaseio.com/"


class License:
    def __init__(self,program:str):
        self.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xFF) for i in range(0, 48, 8)])
        self.program = program
    def check_license(self,username,password):
        url = f"{self.program}/{username}.json"
        license_data = json.loads(requests.get(database_url + url).text)
        if license_data is None : return False
        if bcrypt.checkpw(password.encode(),license_data["password"].encode()): self.update_license(username); return True

    def make_save_file(self,username,password):
        data = {
            "program":self.program,
            "username":username,
            "password":password
        }
        try: os.mkdir("save")
        except: pass
        json.dump(data,open("save/saved.json","w+",errors="ignore"),indent=4)

    def update_license(self,username):
        url = f"{self.program}/{username}.json"
        requests.patch(database_url + url,json={"current-user" : self.mac_address})

    def check_current_user(self,username):
        url = f"{self.program}/{username}/"
        return  self.mac_address == json.loads(requests.get(database_url+url+"current-user.json").text)
    
    def verify_folder(self):
        try: data = json.load(open("save/saved.json","r",errors="ignore")); return self.check_license(data["username"],data["password"])
        except Exception : return False

    def check_user(self,username):
        url = f"{self.program}/{username}.json"
        license_data = json.loads(requests.get(database_url + url).text)
        return license_data["plans"]
    
    def current_use(self,username):
        if not self.check_current_user(username):
            for process in multiprocessing.active_children():process.terminate()
            os._exit(1)
    def checking_repeater(self,username):
        self.current_use(username)
        Timer(15, self.checking_repeater,args=(username,)).start()
        