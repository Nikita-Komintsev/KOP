# sender_app.py
import random
import string
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtNetwork import QTcpSocket

class SenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.message_label = QLabel('Введите сообщение:')
        self.message_edit = QLineEdit()
        self.send_button = QPushButton('Передать')
        self.generate_button = QPushButton('Генерировать случайное сообщение')
        self.sequence_button = QPushButton('Запрос последовательности')

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_edit)
        layout.addWidget(self.send_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.sequence_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.generate_button.clicked.connect(self.generate_random_message)
        self.sequence_button.clicked.connect(self.request_sequence)

        self.socket = QTcpSocket(self)
        self.socket.connectToHost('127.0.0.1', 12345)  # Указать IP-адрес и порт второй программы
        if not self.socket.waitForConnected(1000):
            print('Не удалось подключиться к серверу.')

    def send_message(self):
        message = self.message_edit.text()
        self.socket.write(message.encode())

    def generate_random_message(self):
        message = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.message_edit.setText(message)

    def request_sequence(self):
        # Отправить запрос на последовательность
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = SenderApp()
    sender.show()
    sys.exit(app.exec_())
