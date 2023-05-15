"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets
from a_threads import WeatherHandler

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.latLineEdit = QtWidgets.QLineEdit()
        self.latLabel = QtWidgets.QLabel('Широта')
        self.lonLineEdit = QtWidgets.QLineEdit()
        self.lonLabel = QtWidgets.QLabel('Долгота')
        self.delay = QtWidgets.QLineEdit()
        self.delayLabel = QtWidgets.QLabel('Вермя задержки')
        self.weatherPlainTextLog = QtWidgets.QPlainTextEdit()
        self.weatherLabel = QtWidgets.QLabel('Информация о погоде')
        self.weatherPushButton = QtWidgets.QPushButton('Узнать погоду')

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.latLabel)
        layout.addWidget(self.latLineEdit)
        layout.addWidget(self.lonLabel)
        layout.addWidget(self.lonLineEdit)
        layout.addWidget(self.delayLabel)
        layout.addWidget(self.delay)
        layout.addWidget(self.weatherLabel)
        layout.addWidget(self.weatherPlainTextLog)
        layout.addWidget(self.weatherPushButton)

        self.setLayout(layout)

        self.thread_2 = WeatherHandler(self.latLineEdit.text, self.lonLineEdit.text)
        self.delay.textChanged.connect(self.delayChanged)
        self.thread_2.data_signal.connect(self.onWeatherPushButton)


        self.weatherPushButton.clicked.connect(self.onWeatherPushButton)

    def onWeatherPushButton(self, data):
        lat = self.latLineEdit.text()
        lon = self.lonLineEdit.text()
        self.thread_2.lat = float(lat)
        self.thread_2.lon = float(lon)
        self.lonLineEdit.setEnabled(False)
        self.latLineEdit.setEnabled(False)
        self.delay.setEnabled(False)
        self.thread_2.start()
        self.thread_2.setStatus(True)
        self.weatherPlainTextLog.setPlainText(str(data))

    def delayChanged(self, value):
        self.thread_2.setDelay(int(value))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
