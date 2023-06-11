from .database import Connecter
from .link import Link
from antibot.apis import AntibotApis 

class Core(Connecter,Link):
    """
        Core connecter between all files of database.
        inherit: func.database.Connecter    /   func.link.Link
    """
    def __init__(self,path):
        super().__init__(path)
        Link.__init__(self)
        self.verifier : AntibotApis = AntibotApis()

    def newShortLink(self,url:str,identificator:str):
        new_link = self.addUser("default",identificator)
        if not new_link is None : self.initializeLink(identificator)
        self.pushLink(url,identificator)

    def redirectLink(self,identificator):
        try: return self.notFlagged(self.getLink(identificator))
        except: return "/error"
    
    def notFlagged(self,links) -> str:
        not_flagged:list = [link for link in links if self.verifier.googleSafeBrowsing(link) == True]
        print(not_flagged)
        if bool(not_flagged): return not_flagged[0]
        else : return "/error"

    def generate(self, url,shortner):
        if shortner is None : shortner = super().generate(url)
        self.newShortLink(url=url, identificator=shortner)
        return shortner