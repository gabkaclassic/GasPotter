from numpy import mean
import utilities.postgres as db
from database.tables import __DATA_TABLE, __TEMPERATURE_TABLE, __COEFFICIENTS_TABLE

__STRICT = 10


def check_clients(month):
    def check_clients(month):
        coefficients = db.request(__QUERY_GET_COEFFICIENTS.format(__COEFFICIENTS_TABLE, month))[0]
        coefficient = coefficients[0]
        intercept = coefficients[1]
        correlation = coefficients[2]
        data = db.request(__QUERY_GET_DATA.format(__DATA_TABLE, __TEMPERATURE_TABLE, month, intercept))

        list_id = []
        list_coeff = []

        for client in data:
            list_id.append(client[0])
            list_coeff.append(client[1])
        list_coefficient = [coefficient] * len(list_coeff)
        diffs = list(map(lambda a, b: abs(a - b), list_coefficient, list_coeff))
        diff_id = dict(zip(diffs, list_id))
        diff = mean(diffs)
        print(len(diffs))
        diffs = list(filter(lambda a: a > diff * __STRICT, diffs))
        print(len(diffs))
        suspects = list(filter(lambda a: a is not None, map(lambda a: diff_id.get(a), diffs)))

        return suspects


__QUERY_GET_COEFFICIENTS = '''
    SELECT coefficient, intercept, correlation
    FROM {0}
    WHERE month = {1} 
    AND month NOT IN (6, 7, 8);
'''

__QUERY_GET_DATA = '''
    SELECT d.id AS id,
           ABS((AVG(d.value) - {3})/(AVG(d.area * d_t.different))) AS coefficient
    FROM {0} AS d INNER JOIN {1} d_t on d.date = d_t.date
    WHERE (d.area * d_t.different) <> 0 
    AND EXTRACT(MONTH FROM d.date) = {2} 
    AND EXTRACT(MONTH FROM d.date) NOT IN (6, 7, 8)
    GROUP BY id;
'''
