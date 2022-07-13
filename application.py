from os import environ as env
from testing.test import start
__TEST = env['TEST']

if __TEST:
    start()
else:
    pass