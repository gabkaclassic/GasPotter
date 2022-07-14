import utilities.postgres as db
import database.tables as t
from database.structure_db import filling


def migration():
    created_tables = []
    for table in t.__ALL_TABLES:
        print()
        if not exists(table)[0][0]:
            print(table)
            created_tables.append(table)
            for query in queries.get(table):
                db.request(query)
            print('Table {0} was created'.format(table))

    filling.update_total_coefficients(t.__COEFFICIENTS_TABLE in created_tables)
    print('Coefficients was updated')

    if t.__DATA_TABLE in created_tables:
        print('Data was loaded' if filling.initialize_db() else 'Error of loading data from default file')

    print('Migration was finished')


def exists(table):
    return db.request(__QUERY_CHECK_TABLE_EXIST.format(table))


__QUERY_CHECK_TABLE_EXIST = '''
    SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='{0}');
'''

__QUERIES_CREATE_DATA_TABLE = [
    '''
    CREATE TABLE IF NOT EXISTS {0} (
        id LONG,
        date DATE,
        value FLOAT,
        area FLOAT
    );
    '''.format(t.__DATA_TABLE),
    '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (id, date);
    '''.format(t.__DATA_TABLE),
    '''
    CREATE INDEX IF NOT EXISTS ind_{0}
    ON {0}
    (id, date);
    '''.format(t.__DATA_TABLE)]

__QUERIES_CREATE_TEMPERATURE_TABLE = ['''
    CREATE TABLE IF NOT EXISTS {0} (
        date DATE,
        different FLOAT
    );
    '''.format(t.__TEMPERATURE_TABLE),
    '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (date);
    '''.format(t.__TEMPERATURE_TABLE),
    '''
    CREATE INDEX IF NOT EXISTS ind_{0}
    ON {0}
    (date);  
'''.format(t.__TEMPERATURE_TABLE)]

__QUERIES_CREATE_COEFFICIENTS_TABLE = ['''
    CREATE TABLE IF NOT EXISTS {0} (
        month INT,
        coefficient FLOAT,
        intercept FLOAT,
        correlation FLOAT
    );
    '''.format(t.__COEFFICIENTS_TABLE),
    '''
    AlTER TABLE IF EXISTS {0} 
    ADD CONSTRAINT pk_{0} PRIMARY KEY (month);
    '''.format(t.__COEFFICIENTS_TABLE)]

queries = {
    t.__DATA_TABLE: __QUERIES_CREATE_DATA_TABLE,
    t.__TEMPERATURE_TABLE: __QUERIES_CREATE_TEMPERATURE_TABLE,
    t.__COEFFICIENTS_TABLE: __QUERIES_CREATE_COEFFICIENTS_TABLE
}

migration()