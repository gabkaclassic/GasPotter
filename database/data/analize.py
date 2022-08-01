from numpy import std
from database.structure_db.filling import update_total_coefficients as update_coeff
from psycopg2.sql import SQL as sql, Identifier as ident
import utilities.postgres as db
from database.tables import DATA_TABLE, TEMPERATURE_TABLE, COEFFICIENTS_TABLE


def check_clients(month, strict=20, tails_strict=25):
    coefficients = db.request(QUERY_GET_COEFFICIENTS.format(ident(COEFFICIENTS_TABLE), ident(str(month))))[0]
    coefficient = coefficients[0]
    intercept = coefficients[1]
    data = db.request(QUERY_GET_DATA.format(ident(DATA_TABLE),
                                            ident(TEMPERATURE_TABLE),
                                            ident(str(month)),
                                            ident(str(intercept))
                                            ))
    clients = set()
    for client in data:
        clients.add(Client(client[0], client[1], client[2], client[3], abs(client[3] - coefficient)))

    tails = preparing_output_data(clients, coefficient, intercept, tails_strict, True)
    string_tails = tails['string']
    tails = tails['data']
    coefficients = update_coeff(tails=set(map(lambda c: c.id, tails)))

    coefficient = coefficients['coefficient']
    intercept = coefficients['intercept']
    correlation = coefficients['correlation']

    clients = clients.difference(tails)
    string_suspects = preparing_output_data(clients, coefficient, intercept, strict)['string']

    return {'tails': string_tails, 'suspects': string_suspects, 'trust': correlation}


def preparing_output_data(data, coefficient, intercept, strict, tails=False):

    diff = std(list(map(lambda c: c.diff, data)))
    data = list(filter(lambda c: (c.diff > diff * strict) or ((c.value < 0) and tails), data))

    string = "".join(
        map(
            lambda c: str([c.id, c.value, abs(c.k * coefficient + intercept)]).replace("[", "").replace("]", "").replace(",",
                                                                                                                    ";") + '\n',
            data
        )
    )

    return {'data': data, 'string': string}


QUERY_GET_COEFFICIENTS = sql('''
    SELECT coefficient, intercept, correlation
    FROM {0}
    WHERE month = {1} 
    AND month NOT IN (6, 7, 8);
''')

QUERY_GET_DATA = sql('''
    SELECT d.id AS id, (d.area * d_t.different) AS k, d.value AS value, 
           ABS((AVG(d.value) - {3})/(AVG(d.area * d_t.different))) AS coefficient
    FROM {0} AS d INNER JOIN {1} d_t on d.date = d_t.date
    WHERE (d.area * d_t.different) <> 0
    AND EXTRACT(MONTH FROM d.date) NOT IN (6, 7, 8)
    AND EXTRACT(MONTH FROM d.date) = {2} 
    GROUP BY id, k, value;
''')


class Client:

    def __init__(self, id, k, value, coeff, diff):
        self.id = id
        self.coeff = coeff
        self.diff = diff
        self.value = value
        self.k = k
