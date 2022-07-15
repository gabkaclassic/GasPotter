import pandas as pn
import statsmodels.formula.api as sm
import utilities.postgres as db
from database.tables import DATA_TABLE, TEMPERATURE_TABLE,  COEFFICIENTS_TABLE, DEFAULT_IN_PATH, DEFAULT_FILE
from pathlib import Path


def update_total_coefficients(create=False):
    query_template = QUERY_SAVE_COEFFICIENTS if create else QUERY_UPDATE_COEFFICIENTS

    for month in range(1, 13):

        result = db.request(QUERY_DATA_FROM_TOTAL_COEFFICIENT.format(DATA_TABLE, TEMPERATURE_TABLE, month))

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
            query_template.format(COEFFICIENTS_TABLE, coefficient, intercept, correlation,
                                  month))


def update_db(path=DEFAULT_IN_PATH + '\\' + DEFAULT_FILE, format='CSV', delimiter=';', header=True):
    print(path)
    file = Path(path)
    if file.exists():
        db.request(QUERY_COPY.format(DATA_TABLE, path, format, delimiter, ', HEADER' if header else ''))
        update_total_coefficients()
        return True

    return False


QUERY_DATA_FROM_TOTAL_COEFFICIENT = '''
    SELECT d.value, (d.area * d_t.different) AS k
    FROM {0} AS d INNER JOIN {1} as d_t on d.date=d_t.date
    WHERE EXTRACT(MONTH FROM d.date) = {2};
'''

QUERY_UPDATE_COEFFICIENTS = '''
    UPDATE {0}
    SET coefficient={1}, intercept={2}, correlation={3}
    WHERE month = {4};
'''

QUERY_SAVE_COEFFICIENTS = '''
    INSERT INTO {0}
    (month, coefficient, intercept, correlation) VALUES
    ({4}, {1}, {2}, {3});
'''

QUERY_COPY = '''
    COPY {0} FROM '{1}' WITH (FORMAT {2}, DELIMITER '{3}' {4});
'''