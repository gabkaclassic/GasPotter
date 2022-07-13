import pandas as pn
import statsmodels.formula.api as sm
import utilities.postgres as db
from os import environ as env

__DATA_TABLE = env['DB_DATA_TABLE']
__TEMPERATURE_TABLE = env['DB_TEMPERATURE_TABLE']
__BY_MONTH_TABLE = env['DB_BY_MONTH_TABLE']
__INDIVIDUAL_TABLE = env['DB_INDIVIDUAL_TABLE']
__DEFAULT_PATH = env['DEFAULT_PATH']


def filling_total_coefficient():
    result = db.request(__QUERY_CALCULATE_TOTAL_COEFFICIENT)
    value = []
    coefficient = []

    for data in result:
        value.append(data[0])
        coefficient.append(data[1])
    dates = {
        "value": value,
        "c": coefficient,
    }
    dataframe = pn.DataFrame(dates)
    result = sm.ols(formula="value ~ c", data=dataframe.dropna()).fit()
    coefficient = result.params['c']
    coefficient_correlation = dataframe.dropna().corr()['value']['c']

    # print('Intercept:', result.params['Intercept'], ',', 'coefficient:', coefficient)
    # print('Correlation coefficient: ', coefficient_correlation)

def filling_id_coefficients():
    db.request(__QUERY_INDIVIDUAL)


def filling_month_coefficients():
    db.request(__QUERY_MONTH)


def initialize_db(path=__DEFAULT_PATH, format='CSV', delimiter=';', header=True):
    db.request(__QUERY_COPY.format(__DATA_TABLE, path, format, delimiter, ', HEADER' if header else ''))


__QUERY_CALCULATE_TOTAL_COEFFICIENT = '''
    SELECT d.value, (d.area * d_t.different) AS coefficient
    FROM {0} AS d INNER JOIN {1} as d_t on d.date = d_t.date;
'''.format(__DATA_TABLE, __TEMPERATURE_TABLE)

__QUERY_INDIVIDUAL = '''
    CREATE TABLE {0} AS
    SELECT d.id, AVG(d.area * d_t.different) AS coefficient
    FROM {1} AS d INNER JOIN {2} as d_t on d.date = d_t.date
    group by id;
'''.format(__INDIVIDUAL_TABLE, __DATA_TABLE, __TEMPERATURE_TABLE)

__QUERY_MONTH = '''
    CREATE TABLE {0} AS
    SELECT extract(month from d.date) as month, (AVG(d.area * d_t.different)) AS coefficient
    FROM {1} AS d INNER JOIN {2} as d_t on d.date = d_t.date
    group by d.date; 
'''.format(__BY_MONTH_TABLE, __DATA_TABLE, __TEMPERATURE_TABLE)

__QUERY_COPY = '''
    COPY {0} FROM '{1}' WITH (FORMAT {2}, DELIMITER '{3}' {4});
'''

# filling_total_coefficient()
# filling_id_coefficients()
# filling_month_coefficients()

# initialize_db()
