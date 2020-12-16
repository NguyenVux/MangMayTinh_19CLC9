import sys
import socket
import time
import threading
import copy
import errno
import threading
import socket
import os
import json
import random
from threading import Thread
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QMovie
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui

font = QFont("Arial", 10, 80)
action = ""
result = dict(result="failed")
session_id = None
flag = False


# session_id = self.s.recv(1024).decode()

class Client():
    username = ''
    password = ''
    full_name = ''
    email = ''
    dob = ''
    port = ''
    host = ''
    s = None


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
            os._exit(0)

    def connectServerUI(self, host, port):
        connect_thread = Thread(target=self.connectServer(host, port))
        connect_thread.start()

    def connectServer(self, host, port):
        global session_id
        global client
        ########################## connect ################################
        if host == "" or port == "":
            QMessageBox.information(self, "Warning!", "Do not empty!!!!", QMessageBox.Ok, QMessageBox.Ok)
            self.status.setText("")
        else:
            try:
                client.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = int(port)
                client.s.connect((host, port))
                session_id = client.s.recv(1024).decode()
            except:
                QMessageBox.information(self, "Notification", "Couldn't connect to server", QMessageBox.Ok,
                                        QMessageBox.Ok)
            else:
                choice = QMessageBox.information(self, "Notification", "Connected to server", QMessageBox.Ok,
                                                 QMessageBox.Ok)
                client.host = host
                client.port = port
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
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.UI()
        self.show()

    def UI(self):
        self.initLayout()
        self.mainDesign()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_start = startWindow()

    def initLayout(self):
        self.top_hbox = QHBoxLayout()
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
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText('type your username...')
        form.addRow(username, self.username_entry)

        passwrd = QLabel('Password')
        passwrd.setFont(font)
        self.passwrd_entry = QLineEdit()
        self.passwrd_entry.setEchoMode(QLineEdit.Password)
        self.passwrd_entry.setPlaceholderText('type your password...')
        self.passwrd_entry.returnPressed.connect(self.login)
        form.addRow(passwrd, self.passwrd_entry)

        btn_login = QPushButton("Login")
        btn_login.clicked.connect(self.login)

        btn_registr = QPushButton("Register")
        btn_registr.clicked.connect(self.register)

        self.bot_hbox.addStretch()
        self.bot_hbox.addWidget(btn_registr)
        self.bot_hbox.addWidget(btn_login)
        form.addRow(self.bot_hbox)

        self.main_layout.addLayout(form)

        self.setLayout(self.main_layout)

    def login(self):
        global action
        global session_id
        global client
        global result
        action = "login"
        client.username = self.username_entry.text()
        client.password = self.passwrd_entry.text()

        loginJSON = json.dumps(
            {"uuid": client.username, "pwd": client.password, "action": action, "session_id": session_id})
        client.s.send(loginJSON.encode())
        result = json.loads(client.s.recv(1024).decode())
        if result["result"]:
            client.full_name = result["name"]
            QMessageBox.information(self, "Login successfully!!!!", "Hello, " + client.full_name + " <3",
                                    QMessageBox.Ok, QMessageBox.Ok)
            ########go to chat window################
            self.hide()
            self.main = mainWindow()
        else:
            QMessageBox.information(self, "Fail", "username or password is invalid!!!", QMessageBox.Ok, QMessageBox.Ok)

    def register(self):
        self.hide()
        self.Register = registerWindow()


class registerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Chat Room'
        self.left = 500
        self.top = 300
        self.width = 400
        self.height = 300
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.UI()
        self.show()

    def UI(self):
        self.initLayout()
        self.mainDesign()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.back_login = loginWindow()

    def initLayout(self):
        self.top_hbox = QHBoxLayout()
        self.bot_hbox = QHBoxLayout()
        self.main_layout = QHBoxLayout()

    def mainDesign(self):
        self.form = QFormLayout()

        title_window = QLabel()
        title_window.setText("Register")
        title_window.setFont(QFont("Arial", 20, 100))
        self.top_hbox.addStretch()
        self.top_hbox.addWidget(title_window)
        self.top_hbox.addStretch()
        self.form.addRow(self.top_hbox)

        username = QLabel("Username")
        username.setFont(font)
        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText('Type your username...')
        self.form.addRow(username, self.username_entry)
        self.main_layout.addLayout(self.form)

        passwrd = QLabel("Password")
        passwrd.setFont(font)
        self.passwrd_entry = QLineEdit()
        self.passwrd_entry.setPlaceholderText('Type your password...')
        self.passwrd_entry.setEchoMode(QLineEdit.Password)
        self.form.addRow(passwrd, self.passwrd_entry)
        self.main_layout.addLayout(self.form)

        passwrdConfm = QLabel("Confirm password")
        passwrdConfm.setFont(font)
        self.passwrdConfm_entry = QLineEdit()
        self.passwrdConfm_entry.setPlaceholderText('Type your password again...')
        self.passwrdConfm_entry.setEchoMode(QLineEdit.Password)
        self.form.addRow(passwrdConfm, self.passwrdConfm_entry)
        self.main_layout.addLayout(self.form)
        self.setLayout(self.main_layout)

        name = QLabel('Name')
        name.setFont(font)
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText('Your fullname...')
        self.form.addRow(name, self.name_entry)

        email = QLabel('Email')
        email.setFont(font)
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("example@example.com...")
        self.form.addRow(email, self.email_entry)

        dob = QLabel('Date of birth')
        dob.setFont(font)
        self.dob_entry = QLineEdit()
        self.dob_entry.setPlaceholderText('day month year...')
        self.form.addRow(dob, self.dob_entry)

        regis_btn = QPushButton("Register")
        regis_btn.clicked.connect(self.regisProcessing)
        self.bot_hbox.addStretch()
        self.bot_hbox.addWidget(regis_btn)
        self.form.addRow(self.bot_hbox)
        self.setLayout(self.main_layout)

    ### Register ##############################################################
    def regisProcessing(self):
        global action
        global session_id
        global client
        global result
        action = "register"

        usernm = self.username_entry.text()
        pwrd = self.passwrd_entry.text()
        pwrdCon = self.passwrdConfm_entry.text()
        fullnm = self.name_entry.text()
        eml = self.email_entry.text()
        dob = self.dob_entry.text()
        ################## MAIN REGISTER #########################################
        if usernm == '' or pwrd == '' or pwrdCon == '' or fullnm == '' or eml == '' or dob == '':
            QMessageBox.information(self, "Warning", 'Do not empty!!!!', QMessageBox.Ok, QMessageBox.Ok)
        elif pwrd != pwrdCon:
            QMessageBox.information(self, 'Warning', "Confirm password does not match the password", QMessageBox.Ok,
                                    QMessageBox.Ok)
        else:
            registerJSON = json.dumps({"uuid": usernm, "pwd": pwrd, "action": action,
                                       "session_id": session_id})
            client.s.send(registerJSON.encode())
            result = json.loads(client.s.recv(1024).decode())

            if result["result"]:
                QMessageBox.information(self, "Notification", "Successfull!!!", QMessageBox.Ok, QMessageBox.Ok)
                dataJSON = json.dumps({"name": fullnm, "dob": dob, "email": eml, "action": 'update_info',
                                       "session_id": session_id})
                client.s.send(dataJSON.encode())
                ########## back to login window ############
                self.close()
            else:
                QMessageBox.information(self, 'Warning', "Username is already exist, please try with other username!",
                                        QMessageBox.Ok,
                                        QMessageBox.Ok)


class mainWindow(QWidget):
    def __init__(self):
        global session_id
        super().__init__()
        self.title = 'Chat Room'
        self.left = 500
        self.top = 300
        self.width = 600
        self.height = 600
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.UI()

        self.message_handler = threading.Thread(target=self.handle_messages).start()

    def UI(self):
        self.initLayout()
        self.mainDesign()
        self.show()

    def initLayout(self):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.botLeft_layout = QHBoxLayout()
        self.right_layout = QVBoxLayout()

    def mainDesign(self):
        ################ MENU BAR #############################
        self.bar = QMenuBar()
        file_menu = self.bar.addMenu("File")

        my_profile = QAction("My profile", self)
        file_menu.addAction(my_profile)
        change_pwd = QAction("Change password", self)
        file_menu.addAction(change_pwd)

        change_pwd.triggered.connect(lambda: self.input_handler(change_pwd))

        exit = QAction("Exit", self)
        exit.setShortcut("ctrl+q")
        file_menu.addAction(exit)
        self.main_layout.addWidget(self.bar)

        ################### LAYOUT CHAT #######################
        self.chat_print = QTextEdit()
        self.chat_print.setFocusPolicy(Qt.NoFocus)

        self.chat_entry = QLineEdit()
        self.chat_entry.setPlaceholderText('Type your message...')
        self.chat_entry.returnPressed.connect(lambda: self.input_handler(self.send_btn))

        self.send_btn = QPushButton("Send")
        self.send_btn.setIcon(QIcon('Image/mail-send.png'))
        self.send_btn.clicked.connect(lambda: self.input_handler(self.send_btn))

        self.botLeft_layout.addWidget(self.chat_entry)
        self.botLeft_layout.addWidget(self.send_btn)

        self.left_layout.addWidget(QLabel("[Chat]"))
        self.left_layout.addWidget(self.chat_print)
        self.left_layout.addLayout(self.botLeft_layout)

        info_status = QLabel(f"""
User: {client.username}
Host: {client.host}
Port: {client.port}
        """)
        info_status.setFont(font)

        listOnline_label = QLabel("Online")
        self.listOnline = QListWidget()
        self.listOnline.addItem("all")

        sendFileStatus_label = QLabel("Receiving file status")
        self.listSendFile_status = QListWidget()
        self.sendFile_btn = QPushButton("Send file")

        self.right_layout.addWidget(info_status)
        self.right_layout.addWidget(listOnline_label)
        self.right_layout.addWidget(self.listOnline)
        self.right_layout.addWidget(sendFileStatus_label)
        self.right_layout.addWidget(self.listSendFile_status)
        self.right_layout.addWidget(self.sendFile_btn)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

    # def sendMsg(self, text):
    #     global action
    #     global session_id
    #     me=">>>[me]: "
    #     msg=self.chat_entry.text()
    #     self.chat_print.addItem(text)
    #     self.chat_entry.setText("")

    def handle_messages(self):
        global flag
        global client
        global session_id
        while not flag:
            msg = client.s.recv(1204).decode()
            msg = json.loads(msg)
            if msg["action"] == "status_notify":
                self.listOnline.clear()
                self.listOnline.addItem("all")
                for i in msg["user_list"]:
                    self.listOnline.addItem(i)
            if msg["action"] == "send_msg":
                if msg["sender"]==client.full_name:
                    self.chat_print.append( msg["msg"]+" :ME")
                    self.chat_print.setAlignment(Qt.AlignRight)
                else:
                    self.chat_print.append('[' + msg["sender"] + "]:  " + msg["msg"])
                    self.chat_print.setAlignment(Qt.AlignLeft)

    def input_handler(self, btn):
        global session_id
        global client
        if not btn:
            return
        action = btn.text()
        # Stop Program-------------------------------------------------------------
        if action == "Exit":
            return
        # Change Password----------------------------------------------------------
        if action == "Change password":
            print("Old Pwd")
            old_pwd = input('msg-> ')
            print("New Pwd")
            new_pwd = input('msg-> ')
            print("New Pwd Again")
            new_pwd_2 = input('msg-> ')
            if not new_pwd == new_pwd_2:
                QMessageBox.information(self, "Notification", "new password doesn't match confirm password",
                                        QMessageBox.Ok, QMessageBox.Ok)
            else:
                changeJSON = json.dumps({"pwd": old_pwd, "new_pwd": new_pwd,
                                     "action": "change_pwd", "session_id": session_id})
            client.s.send(changeJSON.encode())
            print(result)
        # Status Notify-----------------------------------------------------------------

        # Send Mess-----------------------------------------------------------------
        if action == "Send":
            username = self.chat_entry.text()
            if not username:
                return
            self.chat_entry.setText('')
            loginJSON = json.dumps(
                {"msg": username, "action": "send_msg", "session_id": session_id, "private_list": []})
            client.s.send(loginJSON.encode())


##############start##############
if __name__ == '__main__':
    client = Client()
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = startWindow()
    os._exit(app.exec_())
