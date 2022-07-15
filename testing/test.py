


def start():
    lines = [1, 2, 321, 12, 21, 212, 1]
    lines = list(map(lambda a: str(a), lines))
    with open('C:/Users/Kuzmi/PycharmProjects/gaspotter/data/output' + '/' + 'suspects.txt', 'w') as f:
        f.writelines(lines)

start()