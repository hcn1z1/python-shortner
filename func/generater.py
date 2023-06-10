import random
import string

def generator():
    letters = string.ascii_letters + string.digits
    return "".join(random.choices(letters,k=6))
