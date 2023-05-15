"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""


from PySide6 import QtWidgets, QtGui, QtCore
from ui.c_signals_events import Ui_Form
import time


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setMouseTracking(True)

        self.ui.pushButtonGetData.clicked.connect(self.getScreenInfo)
        self.ui.pushButtonLB.clicked.connect(self.editPosition)
        self.ui.pushButtonLT.clicked.connect(self.editPosition)
        self.ui.pushButtonRB.clicked.connect(self.editPosition)
        self.ui.pushButtonRT.clicked.connect(self.editPosition)
        self.ui.pushButtonCenter.clicked.connect(self.editPosition)

    def getScreenInfo(self):
        """Получение параметров экрана"""
        screens_count = QtWidgets.QApplication.screens()
        log = self.ui.plainTextEdit.appendPlainText

        log(time.ctime())
        log(f"{11*'='} SystemInfo {11*'='}")
        log(f"Кол-во экранов:           {len(screens_count)}")
        log(f"Основное окно:            {QtWidgets.QApplication.primaryScreen().name()}")
        for cur_screen in screens_count:
            log(f"Разрешение экрана         {cur_screen.name()} составляет {cur_screen.size().width()} на {cur_screen.size().height()}")
        log(f"Окно находится на экране  {QtWidgets.QApplication.screenAt(self.pos()).name()}")
        log(f"Размеры окна:             Ширина {self.size().width()} Высота {self.size().height()}")
        log(f"Минимальные размеры окна: Ширина {self.minimumWidth()} Высота {self.minimumHeight()}")
        log(f"Текущее положение:        x = {self.pos().x()} y = {self.pos().y()}")
        log(f"Центр приложения:         x = {self.pos().x() + self.width()/2} y = {self.pos().y() + self.height()/2}")
        log(f"{30 * '='}\n")

    def editPosition(self):
        """Перемещение экрана на заданную позицию"""
        print(self.sender())
        buttonText = self.sender().text()
        screenWidth = QtWidgets.QApplication.screenAt(self.pos()).size().width()
        screenHeight = QtWidgets.QApplication.screenAt(self.pos()).size().height()

        position = {"Лево/Верх":(0, 0),
                    "Лево/Низ": (0, screenHeight-self.height()-100),
                    "Центр": (screenWidth/2 - self.width()/2, screenHeight/2 - self.height()/2),
                    "Право/Верх": (screenWidth - self.width(), 0),
                    "Право/Низ": (screenWidth- self.width(), screenHeight-self.height()-100)}

        self.move(position.get(buttonText)[0], position.get(buttonText)[1])

    def changeEvent(self, event: QtCore.QEvent) -> None:
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.isMinimized():
                self.ui.plainTextEdit.appendPlainText(time.ctime() + ": window is minimized")
            elif self.isMaximized():
                self.ui.plainTextEdit.appendPlainText(time.ctime() + ": window is maximized")
        if event.type() == QtCore.QEvent.ActivationChange:
            self.ui.plainTextEdit.appendPlainText(time.ctime() + ": window is active")

        QtWidgets.QWidget.changeEvent(self, event)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.ui.plainTextEdit.appendPlainText(time.ctime() + ": window is show")

        QtWidgets.QWidget.showEvent(self, event)

    def hideEvent(self, event: QtGui.QHideEvent) -> None:
        self.ui.plainTextEdit.appendPlainText(time.ctime() + ": window is hide")
        QtWidgets.QWidget.hideEvent(self, event)

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        print(f"moveEvent:   x = {event.pos().x()}, y = {event.pos().y()}")
        QtWidgets.QWidget.moveEvent(self, event)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        print(f"resizeEvent: w = {event.size().width()}, h = {event.size().height()}")
        QtWidgets.QWidget.resizeEvent(self, event)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, "Закрыть окно",
                                                     "Вы хотите закрыть окно?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                     QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
