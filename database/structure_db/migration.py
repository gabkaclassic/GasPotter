from psycopg2.sql import SQL as sql, Identifier as ident

import utilities.postgres as db
import database.tables as t
from database.structure_db import filling


def migration():

    try:
        db.request(QUERY_CREATE_DATABASE)
    except:
        pass
    created_tables = []
    for table in t.ALL_TABLES:
        if not exists(table)[0][0]:
            print(table)
            created_tables.append(table)
            for query in queries.get(table):
                db.request(query)
            print('Table {0} was created'.format(table))

    try:
        filling.update_total_coefficients(t.COEFFICIENTS_TABLE in created_tables)
    except:
        pass
    print('Coefficients was updated')

    if t.DATA_TABLE in created_tables:
        print('Data was loaded' if filling.update_db() else 'Error of loading data from default file')

    print('Migration was finished')


def exists(table):
    return db.request(QUERY_CHECK_TABLE_EXIST.format(ident(table)))


QUERY_CREATE_DATABASE = sql('''
    CREATE DATABASE {0};
''').format(ident(t.DATABASE))

QUERY_CHECK_TABLE_EXIST = sql('''
    SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{0}');
''')

QUERIES_CREATE_DATA_TABLE = [
    sql('''
    CREATE TABLE IF NOT EXISTS {0} (
        id INT,
        date DATE,
        value FLOAT,
        area FLOAT
    );
    ''').format(ident(t.DATA_TABLE)),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    DROP CONSTRAINT IF EXISTS {1};
    ''').format(ident(t.DATA_TABLE), ident(t.DATA_TABLE + '_pkey')),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT {1} PRIMARY KEY (id, date);
    ''').format(ident(t.DATA_TABLE), ident(t.DATA_TABLE + '_pkey')),
    sql('''
    CREATE INDEX IF NOT EXISTS {0}
    ON {1}
    (id, date);
    ''').format(ident(t.DATA_TABLE + '_ind'), ident(t.DATA_TABLE))
]

QUERIES_CREATE_TEMPERATURE_TABLE = [
    sql('''
    CREATE TABLE IF NOT EXISTS {0} (
        date DATE,
        different FLOAT
    );
    ''').format(ident(t.TEMPERATURE_TABLE)),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    DROP CONSTRAINT IF EXISTS {1};
    ''').format(ident(t.TEMPERATURE_TABLE), ident(t.TEMPERATURE_TABLE + '_pkey')),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT {1} PRIMARY KEY (date);
    ''').format(ident(t.TEMPERATURE_TABLE), ident(t.TEMPERATURE_TABLE + '_pkey')),
    sql('''
    CREATE INDEX IF NOT EXISTS {0}
    ON {1}
    (date);  
    ''').format(ident(t.TEMPERATURE_TABLE + '_ind'), ident(t.TEMPERATURE_TABLE))
]

QUERIES_CREATE_COEFFICIENTS_TABLE = [
    sql('''
    CREATE TABLE IF NOT EXISTS {0} (
        month INT,
        coefficient FLOAT,
        intercept FLOAT,
        correlation FLOAT
    );
    ''').format(ident(t.COEFFICIENTS_TABLE)),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    DROP CONSTRAINT IF EXISTS {1};
    ''').format(ident(t.COEFFICIENTS_TABLE), ident(t.COEFFICIENTS_TABLE + '_pkey')),
    sql('''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT {1} PRIMARY KEY (month);
    ''').format(ident(t.COEFFICIENTS_TABLE), ident(t.COEFFICIENTS_TABLE + '_pkey'))
]

queries = {
    t.DATA_TABLE: QUERIES_CREATE_DATA_TABLE,
    t.TEMPERATURE_TABLE: QUERIES_CREATE_TEMPERATURE_TABLE,
    t.COEFFICIENTS_TABLE: QUERIES_CREATE_COEFFICIENTS_TABLE
}

migration()
