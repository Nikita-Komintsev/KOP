# receiver_app.py
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
import random


class ReceiverApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.expected_packets = 0
        self.received_packets = []
        self.loss_percentage = 0

    def initUI(self):
        self.setWindowTitle('receiver')
        self.resize(400, 300)
        self.message_label = QLabel('Полученные сообщения:')
        self.message_display = QLabel()
        self.loss_percentage_label = QLabel('Процент потерь пакетов:')
        self.loss_percentage_spinbox = QSpinBox()
        self.set_loss_percentage_button = QPushButton('Установить процент потерь')
        self.loss_percentage = 0

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_display)
        layout.addWidget(self.loss_percentage_label)
        layout.addWidget(self.loss_percentage_spinbox)
        layout.addWidget(self.set_loss_percentage_button)

        self.setLayout(layout)

        self.set_loss_percentage_button.clicked.connect(self.set_loss_percentage)

        # Устанавливаем диапазон значений для QSpinBox
        self.loss_percentage_spinbox.setRange(0, 100)
        self.loss_percentage_spinbox.setValue(self.loss_percentage)

        self.server = QTcpServer(self)
        self.server.listen(QHostAddress('127.0.0.1'), 12345)  # Указать IP-адрес и порт
        self.server.newConnection.connect(self.new_connection)

    def new_connection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(self.receive_data)

    def receive_data(self):
        client_socket = self.sender()
        data = client_socket.readAll().data().decode()
        packets = json.loads(data)  # Предполагается, что данные приходят в формате JSON
        valid_packets = []
        for packet in packets:
            if random.randint(1, 100) > self.loss_percentage:  # Проверка потери пакета
                valid_packets.append(packet)
            else:print("loss - ", packet)
        print("Received packets:", valid_packets)

        current_text = self.message_display.text()
        self.message_display.setText(f'{current_text}\n{"".join(valid_packets)}')

    def set_loss_percentage(self):
        self.loss_percentage = self.loss_percentage_spinbox.value()
        self.loss_percentage_label.setText(f'Процент потерь пакетов: {self.loss_percentage}%')

    def closeEvent(self, event):
        # Метод, вызываемый при закрытии окна
        self.server.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    receiver = ReceiverApp()
    receiver.show()
    sys.exit(app.exec_())
