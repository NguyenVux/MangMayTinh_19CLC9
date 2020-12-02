import sys
import socket
import time
import threading
from threading import Thread
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui

font = QFont("Arial", 10, 80)


class startWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Test'
        self.left = 500
        self.top = 300
        self.width = 300
        self.height = 150
        self.status = QLabel()
        self.status.resize(40, 40)
        self.initUI()
        self.show()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.setWindowTitle("Chat Room")
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.connectUI()

    def connectUI(self):
        connect_form = QFormLayout()
        hbox_top = QHBoxLayout()
        hbox_mid = QHBoxLayout()
        hbox_down = QHBoxLayout()
        hbox_status = QHBoxLayout()

        p = QPixmap('image/cloud-computing.png')
        image = QLabel()
        image.setPixmap(p)
        hbox_top.addStretch()
        hbox_top.addWidget(image)
        hbox_top.addStretch()
        self.mainLayout.addLayout(hbox_top)

        title = QLabel()
        title.setText("Connect to server")
        title.setFont(QFont("Arial", 20, 100))
        hbox_mid.addStretch()
        hbox_mid.addWidget(title)
        hbox_mid.addStretch()
        connect_form.addRow(hbox_mid)

        host_label = QLabel("Host:")
        host_label.setFont(font)
        host_input = QLineEdit()
        host_input.setPlaceholderText("Type ip address...")
        connect_form.addRow(host_label, host_input)

        port_label = QLabel("Port:")
        port_label.setFont(font)
        port_input = QLineEdit()
        port_input.setPlaceholderText("Type port...")
        connect_form.addRow(port_label, port_input)
        port_input.returnPressed.connect(lambda: self.connectServerUI(host_input.text(), port_input.text()))

        ####status for excuting functions#######
        hbox_status.addStretch()
        hbox_status.addWidget(self.status)
        connect_form.addRow(hbox_status)

        quit_btn = QPushButton("Quit")
        connect_btn = QPushButton("Connect")
        hbox_down.addStretch()
        hbox_down.addWidget(quit_btn)
        hbox_down.addWidget(connect_btn)
        connect_form.addRow(hbox_down)

        quit_btn.clicked.connect(self.exitApp)

        connect_btn.clicked.connect(lambda:
                                    self.connectServerUI(host_input.text(), port_input.text()))
        ########Dislay to screen##########
        self.mainLayout.addLayout(connect_form)
        self.setLayout(self.mainLayout)

    def exitApp(self):
        notify = QMessageBox.information(self, "Notification", "Are you want to exit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if notify == QMessageBox.Yes:
            sys.exit()

    def connectServerUI(self, host, port):
        connect_thread = Thread(target=self.connectServer(host, port))
        connect_thread.start()

    def connectServer(self, host, port):
        ##########connect##########
        if host == "" or port == "":
            QMessageBox.information(self, "Warning!", "Do not empty!!!!", QMessageBox.Ok, QMessageBox.Ok)
            self.status.setText("")
        else:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = int(port)
                self.s.connect((host, port))
            except:
                QMessageBox.information(self, "Notification", "Couldn't connect to server", QMessageBox.Ok,
                                        QMessageBox.Ok)
            else:
                choice = QMessageBox.information(self, "Notification", "Connected to server", QMessageBox.Ok,
                                                 QMessageBox.Ok)
                self.close()
                self.Login = loginWindow()


class loginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Chat Room'
        self.left = 500
        self.top = 300
        self.width = 360
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.UI()
        self.show()

    def UI(self):
        self.initLayout()
        self.mainDesign()

    def closeEvent(self, a0: QtGui.QCloseEvent) :
        self.back_start=startWindow()

    def initLayout(self):
        self.top_hbox = QHBoxLayout()
        self.mid_hbox = QHBoxLayout()
        self.bot_hbox = QHBoxLayout()
        self.main_layout = QHBoxLayout()

    def mainDesign(self):
        form = QFormLayout()

        title_ui = QLabel('Login')
        title_ui.setFont(QFont("Arial", 20, 100))
        self.top_hbox.addStretch()
        self.top_hbox.addWidget(title_ui)
        self.top_hbox.addStretch()
        form.addRow(self.top_hbox)

        username = QLabel('Username')
        username.setFont(font)
        username_entry = QLineEdit()
        username_entry.setPlaceholderText('type your username...')
        form.addRow(username, username_entry)

        passwrd = QLabel('Password')
        passwrd.setFont(font)
        passwrd_entry = QLineEdit()
        passwrd_entry.setEchoMode(QLineEdit.Password)
        passwrd_entry.setPlaceholderText('type your password...')
        form.addRow(passwrd, passwrd_entry)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.login)

        btn_registr = QPushButton("Register")
        # btn_registr.clicked.connect()

        self.bot_hbox.addStretch()
        self.bot_hbox.addWidget(btn_registr)
        self.bot_hbox.addWidget(btn_login)
        form.addRow(self.bot_hbox)

        self.main_layout.addLayout(form)

        self.setLayout(self.main_layout)
    def login(self):
        pass

##############start##############
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = startWindow()
    sys.exit(app.exec_())
