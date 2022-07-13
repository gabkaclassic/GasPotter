import psycopg2 as ps
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from os import environ as env

__USER = env['DB_USER']
__PASSWORD = env['DB_PASSWORD']
__HOST = env['DB_HOST']
__PORT = env['DB_PORT']


def request(query):
    global connection
    result = []

    try:
        connection = ps.connect(user=__USER,
                                password=__PASSWORD,
                                host=__HOST,
                                port=__PORT)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

    except Exception as error:
        print("Error PostgreSQL")
        print(error)
        exit(0)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection was closed")

    return result
