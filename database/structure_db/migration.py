import utilities.postgres as db
import database.tables as t
from database.structure_db import filling


def migration():
    created_tables = []
    for table in t.ALL_TABLES:
        print()
        if not exists(table)[0][0]:
            print(table)
            created_tables.append(table)
            for query in queries.get(table):
                db.request(query)
            print('Table {0} was created'.format(table))

    filling.update_total_coefficients(t.COEFFICIENTS_TABLE in created_tables)
    print('Coefficients was updated')

    if t.DATA_TABLE in created_tables:
        print('Data was loaded' if filling.initialize_db() else 'Error of loading data from default file')

    print('Migration was finished')


def exists(table):
    return db.request(QUERY_CHECK_TABLE_EXIST.format(table))


QUERY_CHECK_TABLE_EXIST = '''
    SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{0}');
'''

QUERIES_CREATE_DATA_TABLE = [
    '''
    CREATE TABLE IF NOT EXISTS {0} (
        id LONG,
        date DATE,
        value FLOAT,
        area FLOAT
    );
    '''.format(t.DATA_TABLE),
    '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (id, date);
    '''.format(t.DATA_TABLE),
    '''
    CREATE INDEX IF NOT EXISTS ind_{0}
    ON {0}
    (id, date);
    '''.format(t.DATA_TABLE)]

QUERIES_CREATE_TEMPERATURE_TABLE = ['''
    CREATE TABLE IF NOT EXISTS {0} (
        date DATE,
        different FLOAT
    );
    '''.format(t.TEMPERATURE_TABLE),
                                      '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (date);
    '''.format(t.TEMPERATURE_TABLE),
                                      '''
    CREATE INDEX IF NOT EXISTS ind_{0}
    ON {0}
    (date);  
'''.format(t.TEMPERATURE_TABLE)]

QUERIES_CREATE_COEFFICIENTS_TABLE = ['''
    CREATE TABLE IF NOT EXISTS {0} (
        month INT,
        coefficient FLOAT,
        intercept FLOAT,
        correlation FLOAT
    );
    '''.format(t.COEFFICIENTS_TABLE),
                                       '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (month);
    '''.format(t.COEFFICIENTS_TABLE)]

queries = {
    t.DATA_TABLE: QUERIES_CREATE_DATA_TABLE,
    t.TEMPERATURE_TABLE: QUERIES_CREATE_TEMPERATURE_TABLE,
    t.COEFFICIENTS_TABLE: QUERIES_CREATE_COEFFICIENTS_TABLE
}
migration()
