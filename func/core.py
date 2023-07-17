from .link import Link
from antibot.apis import AntibotApis 
from .generater import generator

class Core(Link):
    """
        Core connecter between all files of database.
        inherit: func.database.Connecter    /   func.link.Link
    """
    def __init__(self):
        Link.__init__(self)
        self.verifier : AntibotApis = AntibotApis()

    def newShortLink(self,url:str,identificator:str,telegram):
        new_link = None
        self.initializeLink(identificator,telegram)
        self.pushLink(url,identificator)

    def redirectLink(self,identificator):
        try: return self.notFlagged(self.getLink(identificator))
        except Exception as e: print(e);return "/error"
    
    def notFlagged(self,links) -> str:
        not_flagged:list = [link for link in links if self.verifier.googleSafeBrowsing(link) == True]
        if bool(not_flagged): return not_flagged[0]
        else : return "/error"

    def generate(self, url,shortner,telegram =-1):
        if shortner is None : shortner = generator()
        self.newShortLink(url=url, identificator=shortner,telegram=telegram)
        return shortner 