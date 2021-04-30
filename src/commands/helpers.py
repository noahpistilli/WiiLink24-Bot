import random
import string

from datetime import datetime


def generate_random(length: int):
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(length))

    return password


timestamp = datetime.utcnow().strftime('`%H:%M:%S`')
