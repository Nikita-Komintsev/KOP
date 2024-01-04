# sender_app.py
import json
import random
import string
import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox
from PyQt5.QtNetwork import QTcpSocket


class SenderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('sender')
        self.resize(400, 300)
        self.message_label = QLabel('Введите сообщение:')
        self.message_edit = QLineEdit()
        self.num_packets_label = QLabel('Количество пакетов:')
        self.num_packets_spinbox = QSpinBox()
        self.num_packets_spinbox.setMinimum(1)  # Устанавливаем минимальное значение в 1
        self.num_packets_spinbox.setValue(1)  # Устанавливаем значение по умолчанию в 1
        self.send_button = QPushButton('Передать')
        self.generate_button = QPushButton('Генерировать случайное сообщение')
        self.sequence_button = QPushButton('Запрос последовательности')

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_edit)
        layout.addWidget(self.num_packets_label)
        layout.addWidget(self.num_packets_spinbox)
        layout.addWidget(self.send_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.sequence_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)
        self.generate_button.clicked.connect(self.generate_random_message)
        self.sequence_button.clicked.connect(self.request_sequence)

        try:
            # Пытаемся подключиться с повторными попытками
            while not self.connect_to_server():
                print("Не удалось подключиться. Повторная попытка через 5 секунд.")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Соединение закрыто.")

    def connect_to_server(self):
        self.socket = QTcpSocket(self)
        self.socket.connectToHost('127.0.0.1', 12345)  # Указать IP-адрес и порт второй программы
        connected = self.socket.waitForConnected(1000)
        if connected:
            print("Успешное подключение.")
        return connected

    def send_message(self):
        message = self.message_edit.text()
        num_packets = self.num_packets_spinbox.value()

        # Рассчитываем размер пакета и остаток
        packet_size = len(message) // num_packets
        remainder = len(message) % num_packets
        # Формируем пакеты с учетом остатка
        packets = []
        start = 0
        for i in range(num_packets):
            end = start + packet_size + (1 if i < remainder else 0)
            packets.append(message[start:end])
            start = end

        # Отправляем все пакеты в виде массива (используя JSON)
        data_to_send = json.dumps(packets)

        for i, packet in enumerate(packets, start=1):
            print(f'Packet {i}/{len(packets)}: {packet}')  # Display the packet in the console
        self.socket.write(data_to_send.encode())

    def generate_random_message(self):
        message = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        self.message_edit.setText(message)

    def request_sequence(self):
        pass
        # Отправить запрос на последовательность

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = SenderApp()
    sender.show()
    sys.exit(app.exec_())
