import psycopg2
import random
import string

connection = psycopg2.connect(
    database="wl24bot", user='Sketch', password='2006', host='127.0.0.1', port='5432'
)


def generate_random(length: int):
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for i in range(length))

    return password
