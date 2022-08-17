from psycopg2.sql import SQL as sql, Identifier as ident
from database.data.coefficients import calculate_coefficients as calculate
import utilities.postgres as db
from database.tables import DATA_TABLE, TEMPERATURE_TABLE,  COEFFICIENTS_TABLE, DEFAULT_IN_PATH, DEFAULT_FILE
from pathlib import Path
from os.path import join


def update_total_coefficients(create=False, tails={}):
    query_template = QUERY_SAVE_COEFFICIENTS if create else QUERY_UPDATE_COEFFICIENTS
    tails = str(tails).replace("{", "").replace("}", "")
    id_list = tails if len(tails) != 0 else -1

    for month in range(1, 13):
        if month in [6, 7, 8]:
            continue

        result = db.request(QUERY_DATA_FROM_TOTAL_COEFFICIENT.format(
            ident(DATA_TABLE),
            ident(TEMPERATURE_TABLE),
            ident(str(month)),
            ident(str(id_list))
        ))

        value = []
        k = []

        for data in result:
            value.append(data[0])
            k.append(data[1])

        coefficients = calculate(value, k)
        coefficient = coefficients['coefficient']
        intercept = coefficients['intercept']
        correlation = coefficients['correlation']

        db.request(
            query_template.format(ident(COEFFICIENTS_TABLE), ident(str(coefficient)), ident(str(intercept)), ident(str(correlation)),
                                  ident(str(month))))
        return coefficients


def update_db(path=join(DEFAULT_IN_PATH, DEFAULT_FILE), format='CSV', delimiter=';', header=True):
    file = Path(path)
    if file.exists():
        db.request(QUERY_COPY.format(ident(DATA_TABLE), ident(path), ident(format), ident(delimiter), ident(", HEADER") if header else ident("")))
        update_total_coefficients()
        return True

    return False


QUERY_DATA_FROM_TOTAL_COEFFICIENT = sql('''
    SELECT d.value, (d.area * d_t.different) AS k
    FROM {0} AS d INNER JOIN {1} as d_t on d.date=d_t.date
    WHERE d.id NOT IN ({3}) 
    AND EXTRACT(MONTH FROM d.date) = {2}
    AND d.value >= 0;
''')

QUERY_UPDATE_COEFFICIENTS = sql('''
    UPDATE {0}
    SET coefficient={1}, intercept={2}, correlation={3}
    WHERE month = {4};
''')

QUERY_SAVE_COEFFICIENTS = sql('''
    INSERT INTO {0}
    (month, coefficient, intercept, correlation) VALUES
    ({4}, {1}, {2}, {3});
''')

QUERY_COPY = sql('''
    COPY {0} FROM '{1}' WITH (FORMAT {2}, DELIMITER '{3}', ENCODING 'windows-1251' {4});
''')