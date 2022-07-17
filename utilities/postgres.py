import psycopg2 as ps
from os import environ as env

__USER = env['DB_USER']
__PASSWORD = env['DB_PASSWORD']
__HOST = env['DB_HOST']
__PORT = env['DB_PORT']


def request(query):
    result = []
    connection = None
    cursor = None

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
        print(error)
        exit(0)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return result
