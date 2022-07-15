from os import environ as env

FILENAME = env['DEFAULT_OUTPUT_FILENAME']

def write_lines(path, lines):

    with open(path + '/' + FILENAME, 'w+') as f:
        f.writelines(lines)