import psycopg2 as ps
from psycopg2.sql import SQL
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


from configuration.config import ENV

USER = ENV['DB_USER']
PASSWORD = ENV['DB_PASSWORD']
HOST = ENV['DB_HOST']
PORT = ENV['DB_PORT']


def request(query):

    result = []
    connection = None
    cursor = None

    try:
        connection = ps.connect(user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        query = query.as_string(connection).replace('"', '')
        cursor.execute(query)
        connection.commit()

        try:
            result = cursor.fetchall()
        except:
            return

    except Exception as error:
        print(error)
        exit(0)
    finally:
        if connection:
            cursor.close()
            connection.close()

    return result
