import pandas as pn
import statsmodels.formula.api as sm
import utilities.postgres as db
from database.tables import __DATA_TABLE, __TEMPERATURE_TABLE, __DEFAULT_PATH, __COEFFICIENTS_TABLE
from pathlib import Path


def update_total_coefficients(create=False):
    query_template = __QUERY_SAVE_COEFFICIENTS if create else __QUERY_UPDATE_COEFFICIENTS

    for month in range(1, 13):

        result = db.request(__QUERY_DATA_FROM_TOTAL_COEFFICIENT.format(__DATA_TABLE, __TEMPERATURE_TABLE, month))

        value = []
        k = []

        for data in result:
            value.append(data[0])
            k.append(data[1])
        dates = {
            "value": value,
            "c": k,
        }
        dataframe = pn.DataFrame(dates).dropna()
        result = sm.ols(formula="value ~ c", data=dataframe).fit()
        coefficient = result.params['c']
        intercept = result.params['Intercept']
        correlation = dataframe.dropna().corr()['value']['c']

        db.request(
            query_template.format(__COEFFICIENTS_TABLE, coefficient, intercept, correlation,
                                  month))


def initialize_db(path=__DEFAULT_PATH, format='CSV', delimiter=';', header=True):
    file = Path(path)
    if file.exists():
        db.request(__QUERY_COPY.format(__DATA_TABLE, path, format, delimiter, ', HEADER' if header else ''))
        return True

    return False


__QUERY_DATA_FROM_TOTAL_COEFFICIENT = '''
    SELECT d.value, (d.area * d_t.different) AS k
    FROM {0} AS d INNER JOIN {1} as d_t on d.date=d_t.date
    WHERE EXTRACT(MONTH FROM d.date) = {2};
'''

__QUERY_UPDATE_COEFFICIENTS = '''
    UPDATE {0}
    SET coefficient={1}, intercept={2}, correlation={3}
    WHERE month = {4};
'''

__QUERY_SAVE_COEFFICIENTS = '''
    INSERT INTO {0}
    (month, coefficient, intercept, correlation) VALUES
    ({4}, {1}, {2}, {3});
'''

__QUERY_COPY = '''
    COPY {0} FROM '{1}' WITH (FORMAT {2}, DELIMITER '{3}' {4});
'''

# check_clients(2)
# update_total_coefficients()
# initialize_db()
