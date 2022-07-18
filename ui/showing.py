import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui.gui import Ui_Frame
from ui.cui import menu
from configuration.config import ENV

GUI = ENV['GUI']

def show(gui=True):
    if gui:
        start_gui()
    else:
        start_cui()


def start_gui():
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_Frame()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())


def start_cui():
    menu()


func = GUI
# while func != 'y' and func != 'n':
# func = input('Вы хотите использовать графический интерфейс (аналог - консольный интерфейс)[y/n]: ')
show(GUI == 'TRUE')
