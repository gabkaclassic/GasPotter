import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui.ui import Ui_Frame


def show():
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_Frame()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())


show()
