"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()
        self.initSignal()
        self.settings = QtCore.QSettings('Data')
        self.loadData()

    def initUi(self):
        self.dial = QtWidgets.QDial()
        self.dial.setRange(0, 100)
        self.dial.installEventFilter(self)
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem("dec")
        self.comboBox.addItem("hex")
        self.comboBox.addItem("oct")
        self.comboBox.addItem("bin")
        self.LCDNumber = QtWidgets.QLCDNumber()
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(Qt.Orientation.Horizontal)

        layout1 = QtWidgets.QVBoxLayout()
        layout2 = QtWidgets.QHBoxLayout()
        layout3 = QtWidgets.QVBoxLayout()

        layout1.addWidget(self.comboBox)
        layout1.addWidget(self.LCDNumber)

        layout2.addWidget(self.dial)
        layout2.addLayout(layout1)

        layout3.addLayout(layout2)
        layout3.addWidget(self.slider)

        self.setLayout(layout3)

    def initSignal(self):
        self.slider.valueChanged.connect(self.dial.setValue)
        self.slider.valueChanged.connect(self.LCDNumber.display)
        self.dial.valueChanged.connect(self.slider.setValue)
        self.dial.valueChanged.connect(self.LCDNumber.display)

        self.comboBox.currentTextChanged.connect(self.updateLcd)



    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Plus:
            self.dial.setValue(self.dial.value() + 1)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.dial.setValue(self.dial.value() - 1)
        else:
            super().keyPressEvent(event)

    def updateLcd(self):
        if self.comboBox.currentText() == "dec":
            self.LCDNumber.setDecMode()

        elif self.comboBox.currentText() == "bin":
            self.LCDNumber.setBinMode()

        elif self.comboBox.currentText() == "oct":
            self.LCDNumber.setOctMode()

        elif self.comboBox.currentText() == "hex":
            self.LCDNumber.setHexMode()


    def loadData(self):
        self.LCDNumber.display(self.settings.value("Value", ""))
        self.comboBox.setCurrentText(self.settings.value("Text", ""))


    def closeEvent(self, event: QtGui.QCloseEvent):
        self.settings.setValue("Value", self.LCDNumber.intValue())
        self.settings.setValue("Text", self.comboBox.currentText())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
