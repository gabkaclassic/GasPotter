from configuration.config import ENV
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from database.data.analize import check_clients
from database.structure_db.filling import update_db
from utilities.files import write_lines
from datetime import datetime as dt
from os.path import join


class Ui_Frame(object):
    DEFAULT_IN_PATH = ENV['DEFAULT_INPUT_PATH']
    DEFAULT_OUT_PATH = ENV['DEFAULT_OUTPUT_PATH']
    DEFAULT_IN_FILE = ENV['DEFAULT_FILE']
    suspects = []
    tails = []
    HEADER = "ID;Текущий объём;Норма объёма;\n"

    def setupUi(self, Frame):

        Frame.setObjectName("GasPotter")
        Frame.resize(742, 204)

        self.formLayoutWidget = QtWidgets.QWidget(Frame)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 881, 381))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.LoadFileDialog = QFileDialog()
        self.LoadFileDialog.setGeometry(QtCore.QRect(290, 360, 800, 500))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(75)
        self.LoadFileDialog.setFont(font)
        self.LoadFileDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LoadFileDialog.setStyleSheet("")
        self.LoadFileDialog.setDirectory(self.DEFAULT_IN_PATH)
        self.LoadFileDialog.setNameFilter("*.csv")
        self.LoadFileDialog.setViewMode(QFileDialog.Detail)

        self.SelectFileButton = QtWidgets.QPushButton(Frame)
        self.SelectFileButton.setGeometry(QtCore.QRect(450, 100, 211, 47))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.SelectFileButton.setFont(font)
        self.SelectFileButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.SelectFileButton.setStyleSheet("")
        self.SelectFileButton.setObjectName("SelectFileButton")
        self.SelectFileButton.clearFocus()
        self.SelectFileButton.clicked.connect(self.SelectFileButton.setFocus)
        self.SelectFileButton.clicked.connect(self.load_data)

        self.VerticalLine = QtWidgets.QFrame(Frame)
        self.VerticalLine.setGeometry(QtCore.QRect(360, 0, 20, 381))
        self.VerticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.VerticalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VerticalLine.setObjectName("VerticalLine")

        self.AnalizeLabel = QtWidgets.QLabel(Frame)
        self.AnalizeLabel.setGeometry(QtCore.QRect(100, 20, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AnalizeLabel.setFont(font)
        self.AnalizeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AnalizeLabel.setObjectName("AnalizeLabel")

        self.HorizontalLine = QtWidgets.QFrame(Frame)
        self.HorizontalLine.setGeometry(QtCore.QRect(0, 40, 741, 16))
        self.HorizontalLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.HorizontalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HorizontalLine.setObjectName("HorizontalLine")

        self.StrictLabel = QtWidgets.QLabel(Frame)
        self.StrictLabel.setGeometry(QtCore.QRect(10, 110, 141, 47))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.StrictLabel.setFont(font)
        self.StrictLabel.setObjectName("StrictLabel")

        self.StrictSlider = QtWidgets.QSlider(Frame)
        self.StrictSlider.setGeometry(QtCore.QRect(170, 130, 121, 16))
        self.StrictSlider.setOrientation(QtCore.Qt.Horizontal)
        self.StrictSlider.setObjectName("StrictSlider")
        self.StrictSlider.setRange(1, 200)
        self.StrictSlider.setValue(10)
        self.StrictSlider.setSingleStep(1)
        self.StrictSlider.sliderMoved.connect(self.change_strict_edit)

        self.StrictEdit = QtWidgets.QLineEdit(Frame)
        self.StrictEdit.setGeometry(QtCore.QRect(300, 120, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.StrictEdit.setFont(font)
        self.StrictEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.StrictEdit.setObjectName("StrictEdit")
        self.StrictEdit.setText(str(1))
        self.StrictEdit.editingFinished.connect(self.change_strict_slider)

        self.LoadLabel = QtWidgets.QLabel(Frame)
        self.LoadLabel.setGeometry(QtCore.QRect(470, 20, 161, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.LoadLabel.setFont(font)
        self.LoadLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LoadLabel.setObjectName("LoadLabel")

        self.DateLabel = QtWidgets.QLabel(Frame)
        self.DateLabel.setGeometry(QtCore.QRect(10, 50, 291, 47))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DateLabel.setFont(font)
        self.DateLabel.setObjectName("DateLabel")

        self.AnalizeButton = QtWidgets.QPushButton(Frame)
        self.AnalizeButton.setGeometry(QtCore.QRect(70, 170, 211, 25))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.AnalizeButton.setFont(font)
        self.AnalizeButton.setStyleSheet("")
        self.AnalizeButton.setObjectName("AnalizeButton")
        self.AnalizeButton.clicked.connect(self.search_suspects)

        self.AnalizeFileDialog = QFileDialog()
        self.AnalizeFileDialog.setGeometry(QtCore.QRect(290, 360, 800, 500))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(75)
        self.AnalizeFileDialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.AnalizeFileDialog.setStyleSheet("")
        self.AnalizeFileDialog.setDirectory(self.DEFAULT_OUT_PATH)
        self.AnalizeFileDialog.setFileMode(QFileDialog.DirectoryOnly)

        self.MonthBox = QtWidgets.QSpinBox(Frame)
        self.MonthBox.setGeometry(QtCore.QRect(300, 60, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.MonthBox.setFont(font)
        self.MonthBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MonthBox.setObjectName("MonthBox")
        self.MonthBox.setRange(1, 12)
        self.MonthBox.setValue(dt.now().month)

        self.CorrelationLabel = QtWidgets.QLabel(Frame)
        self.CorrelationLabel.setGeometry(QtCore.QRect(10, 90, 291, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.CorrelationLabel.setFont(font)
        self.CorrelationLabel.setObjectName("CorrelationLabel")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("GasPotter", "GasPotter"))
        self.SelectFileButton.setText(_translate("Frame", "Загрузить новые данные\n"
                                                          "(только CSV-файлы)"))
        self.DateLabel.setText(_translate("Frame", "Выберите номер месяца (не летнего):"))
        self.AnalizeButton.setText(_translate("Frame", "Проанализировать данные"))
        self.AnalizeLabel.setText(_translate("Frame", "Анализ данных"))
        self.StrictLabel.setText(_translate("Frame", "Строгость оценки:"))
        self.LoadLabel.setText(_translate("Frame", "Загрузка данных"))
        self.StrictEdit.setText(_translate("Frame", str(self.StrictSlider.value())))
        self.CorrelationLabel.setText(_translate("Frame", "Корреляция:"))

    def change_strict_edit(self):
        self.StrictEdit.setText(str(self.StrictSlider.value() / 10))

    def change_strict_slider(self):
        try:
            strict = round(float(self.StrictEdit.text()), 1)
        except ValueError:
            strict = 10
            self.StrictEdit.setText(str(strict))

        self.StrictSlider.setValue(strict * 10)

    def search_suspects(self):

        path = QFileDialog.getExistingDirectory(self.AnalizeFileDialog, "Выбрать папку").strip()
        if self.MonthBox.value() not in [6, 7, 8]:
            result = check_clients(self.MonthBox.value(), self.StrictSlider.value() / 10, self.StrictSlider.value() / 10)
            tails = self.HEADER + result['tails']
            suspects = self.HEADER + result['suspects']
            trust = result['trust']
            self.CorrelationLabel.setText('Корреляция: {0}%'.format(int(trust * 100)))
            write_lines(self.DEFAULT_OUT_PATH if len(path) == 0 else path, suspects, "Suspects.txt")
            write_lines(self.DEFAULT_OUT_PATH if len(path) == 0 else path, tails, "Tails.txt")
        else:
            self.CorrelationLabel.setText('Корреляция: ???% - вы ввели летний месяц')

    def load_data(self):
        self.LoadFileDialog.setDirectory(self.DEFAULT_IN_PATH)
        self.LoadFileDialog.setNameFilter("*.csv")
        self.LoadFileDialog.setViewMode(QFileDialog.Detail)
        path = ''
        try:
            path = QFileDialog.getOpenFileName(self.LoadFileDialog, "Выбрать файл")[0]
        except:
            path = join(self.DEFAULT_IN_PATH, self.DEFAULT_IN_FILE)

        update_db(path=path)
