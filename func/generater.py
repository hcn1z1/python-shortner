import random
import string,re

def generator():
    letters = string.ascii_letters + string.digits
    return "".join(random.choices(letters,k=6))

def valideUrl(url) -> bool:
    pattern = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')
    return bool(re.match(pattern, url))