
def write_lines(path, lines, filename):
    with open(path + '/' + filename, 'w+') as f:
        f.writelines(lines)


def read_lines(path):

    with open(path, 'r') as f:
        lines = f.readlines()

    return lines
