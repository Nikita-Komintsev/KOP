# sender_app.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog
from PyQt5.QtNetwork import QTcpSocket
import random

class SenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.message_label = QLabel('Введите сообщение:')
        self.message_edit = QLineEdit()
        self.send_button = QPushButton('Передать')
        self.sequence_button = QPushButton('Запрос последовательности')
        self.loss_percentage, _ = QInputDialog.getInt(self, 'Настройки', 'Процент потерь пакетов:', 0, 0, 100)

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_edit)
        layout.addWidget(self.send_button)
        layout.addWidget(self.sequence_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.sequence_button.clicked.connect(self.request_sequence)

        self.socket = QTcpSocket(self)
        self.socket.connectToHost('127.0.0.1', 12345)  # Указать IP-адрес и порт второй программы
        if not self.socket.waitForConnected(1000):
            print('Не удалось подключиться к серверу.')

    def send_message(self):
        message = self.message_edit.text()
        if random.randint(1, 100) > self.loss_percentage:  # Моделирование потерь пакетов
            self.socket.write(message.encode())

    def request_sequence(self):
        pass
        # Отправить запрос на последовательность

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = SenderApp()
    sender.show()
    sys.exit(app.exec_())
