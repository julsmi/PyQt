"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets
from a_threads import SystemInfo

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delayLineEdit = QtWidgets.QLineEdit()
        self.CPULabel = QtWidgets.QLabel()
        self.RAMLabel = QtWidgets.QLabel()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.delayLineEdit)
        layout.addWidget(self.CPULabel)
        layout.addWidget(self.RAMLabel)

        self.setLayout(layout)

        self.delayLineEdit.textChanged.connect(self.delayPushButtonClicked)

        self.thread_1 = SystemInfo()
        self.thread_1.start()
        self.thread_1.systemInfoReceived.connect(self.onSystemInfoReceived)


    def delayPushButtonClicked(self, value):
        self.thread_1.delay = int(value)

    def onSystemInfoReceived(self, value_list):
        cpu_usage = value_list[0]
        ram_usage = value_list[1]
        self.CPULabel.setText(f"CPU usage: {cpu_usage} %")
        self.RAMLabel.setText(f"RAM usage: {ram_usage} %")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
