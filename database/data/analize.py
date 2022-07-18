from numpy import mean
from psycopg2.sql import SQL as sql, Identifier as ident
import utilities.postgres as db
from database.tables import DATA_TABLE, TEMPERATURE_TABLE, COEFFICIENTS_TABLE


def check_clients(month, strict):
    coefficients = db.request(QUERY_GET_COEFFICIENTS.format(ident(COEFFICIENTS_TABLE), ident(str(month))))[0]
    coefficient = coefficients[0]
    intercept = coefficients[1]
    correlation = coefficients[2]
    data = db.request(QUERY_GET_DATA.format(ident(DATA_TABLE), ident(TEMPERATURE_TABLE), ident(str(month)), ident(str(intercept))))

    list_id = []
    list_coeff = []

    for client in data:
        list_id.append(client[0])
        list_coeff.append(client[1])
    list_coefficient = [coefficient] * len(list_coeff)
    diffs = list(map(lambda a, b: abs(a - b), list_coefficient, list_coeff))
    diff_id = dict(zip(diffs, list_id))
    diff = mean(diffs)
    diffs = list(filter(lambda a: a > diff * strict, diffs))
    suspects = list(filter(lambda a: a is not None, map(lambda a: diff_id.get(a), diffs)))
    suspects = list(map(lambda a: str(a) + '\n', suspects))

    return {'suspects': suspects, 'trust': correlation}


QUERY_GET_COEFFICIENTS = sql('''
    SELECT coefficient, intercept, correlation
    FROM {0}
    WHERE month = {1} 
    AND month NOT IN (6, 7, 8);
''')

QUERY_GET_DATA = sql('''
    SELECT d.id AS id,
           ABS((AVG(d.value) - {3})/(AVG(d.area * d_t.different))) AS coefficient
    FROM {0} AS d INNER JOIN {1} d_t on d.date = d_t.date
    WHERE (d.area * d_t.different) <> 0 
    AND EXTRACT(MONTH FROM d.date) = {2} 
    AND EXTRACT(MONTH FROM d.date) NOT IN (6, 7, 8)
    GROUP BY id;
''')
