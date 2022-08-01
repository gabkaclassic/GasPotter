import os
from os import path
from utilities.files import read_lines as rl


CONFIGURATION_FILENAME = 'env.txt'

def load_env():
    dir = os.path.abspath(os.curdir)

    if not os.path.exists(path.join(dir, CONFIGURATION_FILENAME)):
        dir = path.abspath(path.join(dir, 'configuration', CONFIGURATION_FILENAME))
    lines = rl(dir)
    lines = list(map(lambda s: s.replace('\n', ''), lines))
    lines = list(filter(lambda s: len(s) > 0, lines))

    return dict(map(lambda l: [l[:l.index('=')], l[l.index('=') + 1:]], lines))


ENV = load_env()


