import random
import string

import sqlite3
from database.generator import *


def gen_random_price():
    """
    Generate random prices for products in range 10-1000
    :return:
    """
    return round(random.uniform(10, 1000),2)


def gen_random_name():
    """
    Generate random names for products
    :return:
    """
    name = []
    for i in range(8):
        name.append(random.choice(string.ascii_lowercase))
    return "".join(name)


def gen_random_desc():
    """
    Generate desc sentences for products
    :return:
    """
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs")
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    num = random.randrange(0,5)
    return nouns[num] + ' ' + verbs[num] + ' ' + adj[num] + ' ' + adv[num]

# print(gen_random_name(), gen_random_price(), gen_random_desc())


def insert_data(n):
    """
    Insert N rows into the database of dummy data
    :param n:
    :return:
    """
    conn = sqlite3.connect('../database.db')

    cur = conn.cursor()
    for i in range(n):
        try:
            cur.execute('INSERT INTO products (description, price, name) VALUES (?,?,?);',(gen_random_desc(), gen_random_price(), gen_random_name()))
            print("Entry {} successful".format(i))
        except:
            conn.rollback()
            print("Error in {} entry".format(i))
    conn.commit()
    conn.close()

# insert_data(100)


def get_all_data():
    conn = sqlite3.connect("../database.db")
    # conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("select * from products")
    rows = cur.fetchall()
    print(rows)

get_all_data()
