# receiver_app.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QHostAddress


class ReceiverApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.message_label = QLabel('Полученные сообщения:')
        self.message_display = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_display)

        self.setLayout(layout)

        self.server = QTcpServer(self)
        self.server.listen(QHostAddress('127.0.0.1'), 12345)  # Указать IP-адрес и порт
        self.server.newConnection.connect(self.new_connection)

    def new_connection(self):
        client_socket = self.server.nextPendingConnection()
        client_socket.readyRead.connect(self.receive_data)

    def receive_data(self):
        client_socket = self.sender()
        data = client_socket.readAll().data().decode()
        self.message_display.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    receiver = ReceiverApp()
    receiver.show()
    sys.exit(app.exec_())
