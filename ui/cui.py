import os.path

from past.builtins import raw_input

from configuration.config import ENV
from os import system as sys
from database.data.analize import check_clients
from database.structure_db.filling import update_db
from utilities.files import write_lines

DEFAULT_IN_PATH = ENV['DEFAULT_INPUT_PATH']
DEFAULT_OUT_PATH = ENV['DEFAULT_OUTPUT_PATH']
DEFAULT_IN_FILE = ENV['DEFAULT_FILE']
HEADER = "ID;Текущий объём;Норма объёма;\n"

MENU = '''
============================================
            Выберите функцию:
============================================
    (1) - Загрузить новые данные в базу
    (2) - Проанализировать данные
    (0) - Выход из консоли 
--------------------------------------------
В случае неправильного выбора функции вы 
можете вернуться в главное меню нажав (n)
--------------------------------------------    
'''


def menu():
    fun = 1
    while fun != 0:
        clear()
        try:
            fun = int(raw_input('Функция: '))
            if fun == 1:
                load_data()
            elif fun == 2:
                analyze()
            elif fun != 0:
                print('Пожалуйста, выберите функцию из предложенного списка')
                continue
        except ValueError:
            fun = 9
            print('Пожалуйста, выберите функцию из предложенного списка')
            continue
    print('Выход из программы...')


def load_data():
    clear()
    path = input('Ведите полный путь до файла (по умолчанию будет выбран файл {0}: '.format(
        os.path.join(DEFAULT_IN_PATH, DEFAULT_IN_FILE)))
    path = DEFAULT_IN_PATH if len(path.strip()) == 0 else path.strip()
    if path == 'n':
        menu()
    update_db(path=path)
    print('Данные успешно загружены')


def analyze():
    clear()
    path = input('Ведите полный путь папки (по умолчанию будет выбрана папка {0}: '.format(DEFAULT_OUT_PATH))
    path = DEFAULT_OUT_PATH if len(path.strip()) == 0 else path.strip()
    if path == 'n':
        menu()
    month = 0
    while month == 0:
        try:
            i = input('Введите номер месяца (при вводе летних месяцев (6-8) вероятность корректности данных '
                      'значительно снижается): ')
            if i == 'n':
                menu()
            month = int(i)
        except ValueError:
            print('Месяц введён некорректно')
            month = 0
            continue

    try:
        i = input('Введите уровень строгости оценки (0.1 - 20.0, значение по-умолчанию 10): ')
        if i == 'n':
            menu()
        strict = float(i)
    except ValueError:
        print('Выбрано значение по-умолчанию')
        strict = 10.0

    print('...')
    result = check_clients(month, strict, strict)
    suspects = HEADER + result['suspects']
    tails = HEADER + result['tails']
    trust = result['trust']
    write_lines(DEFAULT_OUT_PATH if len(path) == 0 else path, suspects, "Suspects.txt")
    write_lines(DEFAULT_OUT_PATH if len(path) == 0 else path, tails, "Tails.txt")
    print('Данные о клиентах загружены (всего {0} выделено, данным можно верить ~ на {1}%'.format(
        len(suspects), int(trust * 100)))


def clear():
    try:
        sys('cls')
    except:
        sys('clear')
