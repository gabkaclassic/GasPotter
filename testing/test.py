import os.path
from os import system as sys
from psycopg2.sql import SQL as sql, Identifier as ident

def start():
    s1 = {1, 2 ,3 ,5 , 345,34 ,5}
    s2 = {1, 3, 5}
    print(s1.difference(s2))



start()