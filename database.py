import psycopg2 as ps
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from os import environ as env

class DB:

    _USER = env['DB_USER']
    _PASSWORD = env['DB_PASSWORD']
    _HOST = env['DB_HOST']
    _PORT = env['DB_PORT']

    def request(self, query=''):

        global cursor
        global connection
        global result

        try:
            connection = ps.connect(user=self._USER,
                                    password=self._PASSWORD,
                                    host=self._HOST,
                                    port=self._PORT)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except (Exception) as error:
            print("Error PostgreSQL", error)
            print(error)
            exit(0)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection was closed")

        return result
