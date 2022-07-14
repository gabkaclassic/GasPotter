import psycopg2 as ps
from os import environ as env

__USER = env['DB_USER']
__PASSWORD = env['DB_PASSWORD']
__HOST = env['DB_HOST']
__PORT = env['DB_PORT']

__connection = None


def request(query):

    result = []

    try:
        connection = ps.connect(user=__USER,
                                password=__PASSWORD,
                                host=__HOST,
                                port=__PORT)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        if str(query).strip().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            return

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
