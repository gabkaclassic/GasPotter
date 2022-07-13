import requests as rq
from os import environ as env

_BASE = 'http://history.openweathermap.org/data/2.5/history/'
_TYPE = 'day'
_START_DATE = '1612137600'
_END_DATE = '1612223999'
_CITY = 'lat=57.7665&lon=40.9269'


def get_temperature(base=_BASE,
                    city=_CITY,
                    type=_TYPE,
                    start_date=_START_DATE,
                    end_date=_END_DATE,
                    key=env['WEATHER_KEY']):
    get_query = base + 'city?' + city \
                + '&type=' + type \
                + '&start=' + start_date \
                + '&end=' + end_date \
                + '&appid=' + key
    result = rq.get(get_query)

    return result
