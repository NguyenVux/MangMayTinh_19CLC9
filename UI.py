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
from PyQt5.QtGui import QIcon, QTextDocument, QTextOption, QColor
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import json_util
import action_util
import FTP_Client

font = QFont("Arial", 10, 80)
action = ""
result = dict(result="failed")
session_id = None
flag = False
userOnline = []

USER_ME = 0
USER_THEM = 1

BUBBLE_COLORS = {USER_ME: "#90caf9", USER_THEM: "#a5d6a7"}
USER_TRANSLATE = {USER_ME: QPoint(20, 0), USER_THEM: QPoint(0, 0)}

BUBBLE_PADDING = QMargins(15, 5, 35, 5)
TEXT_PADDING = QMargins(25, 15, 45, 15)


class MessageDelegate(QStyledItemDelegate):
    """
    Draws each message.
    """

    _font = None

    def paint(self, painter, option, index):
        painter.save()
        # Retrieve the user,message uple from our model.data method.
        user, text = index.model().data(index, Qt.DisplayRole)

        trans = USER_TRANSLATE[user]
        painter.translate(trans)

        # option.rect contains our item dimensions. We need to pad it a bit
        # to give us space from the edge to draw our shape.
        bubblerect = option.rect.marginsRemoved(BUBBLE_PADDING)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        # draw the bubble, changing color + arrow position depending on who
        # sent the message. the bubble is a rounded rect, with a triangle in
        # the edge.
        painter.setPen(Qt.NoPen)
        color = QColor(BUBBLE_COLORS[user])
        painter.setBrush(color)
        painter.drawRoundedRect(bubblerect, 10, 10)

        # draw the triangle bubble-pointer, starting from the top left/right.
        if user == USER_ME:
            p1 = bubblerect.topRight()
        else:
            p1 = bubblerect.topLeft()
        painter.drawPolygon(p1 + QPoint(-20, 0), p1 + QPoint(20, 0), p1 + QPoint(0, 20))

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        # draw the text
        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        painter.translate(textrect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        _, text = index.model().data(index, Qt.DisplayRole)
        textrect = option.rect.marginsRemoved(TEXT_PADDING)

        toption = QTextOption()
        toption.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        doc = QTextDocument(text)
        doc.setTextWidth(textrect.width())
        doc.setDefaultTextOption(toption)
        doc.setDocumentMargin(0)

        textrect.setHeight(int(doc.size().height()))
        textrect = textrect.marginsAdded(TEXT_PADDING)
        return textrect.size()


class MessageModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)
        self.messages = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # Here we pass the delegate the user, message tuple.
            return self.messages[index.row()]

    def setData(self, index, role, value):
        self._size[index.row()]

    def rowCount(self, index):
        return len(self.messages)

    def add_message(self, who, text):
        """
        Add an message to our message list, getting the text from the QLineEdit
        """
        if text:  # Don't add empty strings.
            # Access the list via the model.
            self.messages.append((who, text))
            # Trigger refresh.
            self.layoutChanged.emit()


class Client():
    username = ''
    password = ''
    full_name = ''
    email = ''
    dob = ''
    port = ''
    host = ''
    s = None


def Diff(li1, li2):
    return (list(list(set(li1) - set(li2)) + list(set(li2) - set(li1))))


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
        # client.s.send(loginJSON.encode())
        json_util.send(loginJSON, client.s)
        # result = json.loads(client.s.recv(1024).decode())
        result = json.loads(json_util.receive(client.s).decode())
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
            json_util.send(registerJSON, client.s)
            result = json.loads(json_util.receive(client.s).decode())

            if result["result"]:
                QMessageBox.information(self, "Notification", "Successfull!!!", QMessageBox.Ok, QMessageBox.Ok)
                dataJSON = json.dumps({"uuid": usernm, "name": fullnm, "dob": dob, "email": eml, "action": 'update_info',
                                       "session_id": session_id})
                json_util.send(dataJSON, client.s)

                ########## back to login window ############
                self.close()
            else:
                QMessageBox.information(self, 'Warning', "Username is already exist, please try with other username!",
                                        QMessageBox.Ok,
                                        QMessageBox.Ok)


class mainWindow(QWidget):
    def __init__(self):
        global session_id
        self.d = Communicate()
        self.d.file_percent.connect(self.set_value_upload)
        super().__init__()
        self.title = 'Chat Room'
        self.left = 500
        self.top = 300
        self.width = 700
        self.height = 700
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
        self.main_layout = QVBoxLayout()
        self.h_layout = QHBoxLayout()
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
        my_profile.triggered.connect(lambda: self.input_handler(my_profile))

        exit = QAction("Exit", self)
        exit.setShortcut("ctrl+q")
        file_menu.addAction(exit)
        self.main_layout.addWidget(self.bar)
        ######## FIND PROFILE LAYOUT ############
        form_find = QHBoxLayout()
        self.find_profile = QLineEdit()
        self.find_profile.setPlaceholderText("Find profile of an user")
        self.main_layout.addWidget(self.find_profile)
        findPf_btn = QPushButton("Find profile")

        self.find_profile.returnPressed.connect(lambda: self.input_handler(findPf_btn))
        findPf_btn.clicked.connect(lambda: self.input_handler(findPf_btn))
        form_find.addWidget(self.find_profile, 30)
        form_find.addWidget(findPf_btn, 40)
        self.main_layout.addLayout(form_find)
        ################### LAYOUT CHAT #######################
        self.chat_print = QListView()
        self.chat_print.setItemDelegate(MessageDelegate())
        self.model = MessageModel()
        self.chat_print.setModel(self.model)

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
# layout view user online list -------------------------------------------------------
        listOnline_label = QLabel("Online")
        self.listOnline = QListWidget()
        self.listOnline.addItem("all")
# layout upload and download file------------------------------------------------------
        upload_lb=QLabel("Upload")
        upload_lb.setFont(font)
        self.upload_entry = QLineEdit()
        self.upload_entry.setPlaceholderText("URL OF FILE")
        self.upload_entry.setReadOnly(True)
        upload_btn = QPushButton("Upload file")
        upload_btn.clicked.connect(self.upload_file)
        self.upload_bar = QProgressBar()

        download_lb=QLabel("Download")
        download_lb.setFont(font)
        self.download_entry = QLineEdit()
        self.download_entry.setPlaceholderText("Enter name of the file saved in server")
        download_btn = QPushButton("Download")
        self.download_bar = QProgressBar()

        self.private_list = QComboBox()# input receiver
# Add layout --------------------------------------------------------
        self.right_layout.addWidget(info_status)
        self.right_layout.addWidget(listOnline_label)
        self.right_layout.addWidget(self.listOnline)

        self.right_layout.addWidget(upload_lb)
        self.right_layout.addWidget(self.upload_entry)
        self.right_layout.addWidget(self.upload_bar)
        self.right_layout.addWidget(upload_btn)

        self.right_layout.addWidget(download_lb)
        self.right_layout.addWidget(self.download_entry)
        self.right_layout.addWidget(self.download_bar)
        self.right_layout.addWidget(download_btn)

        self.right_layout.addWidget(self.private_list)

        self.h_layout.addLayout(self.left_layout)
        self.h_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.h_layout)

        self.setLayout(self.main_layout)

    def handle_messages(self):
        global flag
        global client
        global session_id
        global userOnline

        printer = Communicate()
        printer.print_chat.connect(self.addMsg)
        printer.print_info.connect(self.findProfile)

        while not flag:
            # msg = client.s.recv(1204).decode()
            msg = json_util.receive(client.s).decode()
            msg = json.loads(msg)
            if msg["action"] == "status_notify":
                list_online = []
                list_filter = []
                self.listOnline.clear()
                self.private_list.clear()
                self.private_list.addItem("all")
                for i in msg["user_list"]:
                    self.listOnline.addItem(i)
                    self.private_list.addItem(i)
                    list_online.append(i)
                if not userOnline:
                    userOnline = list_online
                else:
                    list_filter = Diff(userOnline, list_online)
                    for i in list_filter:
                        if i in userOnline:
                            printer.print_chat.emit(USER_THEM, "[server]: " + i + " left")
                    userOnline = list_online
            if msg["action"] == "send_msg":
                if msg["sender"] == client.full_name:
                    printer.print_chat.emit(USER_ME, msg['msg'])
                else:
                    if msg["private"] == 1:
                        printer.print_chat.emit(USER_THEM, msg['sender'] + " (private): " + msg['msg'])
                    else:
                        printer.print_chat.emit(USER_THEM, msg['sender'] + ": " + msg['msg'])
            if msg["action"] == action_util.Action.view_info:
                print(msg)
                printer.print_info.emit(msg)

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
            self.changepwd()
        # Send Mess-----------------------------------------------------------------
        if action == "Send":
            username = self.chat_entry.text()
            if not username:
                return
            self.chat_entry.setText('')
            receiver = self.private_list.currentText()
            if receiver == 'all' or not receiver:
                chatJson = json.dumps(
                    {"msg": username, "action": "send_msg", "session_id": session_id,
                     "private_list": []})
            else:
                chatJson = json.dumps(
                    {"msg": username, "action": "send_msg", "session_id": session_id,
                     "private_list": [self.private_list.currentText()]})
            # client.s.send(loginJSON.encode())
            receiver = self.private_list.currentText()
            if receiver != "all" and receiver:
                self.addMsg(USER_ME, username)
            print(chatJson)
            json_util.send(chatJson, client.s)
        # view info -----------------------------------------------------------
        if action == "My profile" or action == "Find profile" and self.find_profile.text():
            profileJSON = json.dumps(
                {"uuid": self.find_profile.text(), "action": action_util.Action.view_info, "session_id": session_id})
            json_util.send(profileJSON, client.s)
        # update info -----------------------------------------------------------------
        if action == "Update profile":
            updateJSON = json.dumps(
                {"name": client.full_name, "dob": client.dob, "email": client.email, "session_id": session_id})
            json_util.send(updateJSON, client.s)

    def changepwd(self):
        self.changePw_wd = changePwdWindown()

    def addMsg(self, user, msg):
        self.model.add_message(user, msg)
        self.chat_print.scrollToBottom()

    def myProfile(self):
        self.my_prof = myProfileWindow()

    def findProfile(self, profile):
        self.find_profile.setText("")
        try:
            inform = f"""
Name: {profile['name']}
Date of birth: {profile['dob']}
email: {profile['email']}
            """
        except:
            QMessageBox.information(self, "ERROR", "Not found!!!!", QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.information(self, profile["uuid"], inform, QMessageBox.Ok, QMessageBox.Ok)

    def upload_file(self):
        url = QFileDialog.getOpenFileName(self, "Choose a file", "", "All Files(*)")
        self.upload_entry.setText(url[0])

        if url:
            list_file = url[0].rsplit("/", 1)
            ftp_sock = FTP_Client.FTPClient(client.host, client.port + 1)
            #ftp_sock.send_file(list_file[1], list_file[0], self.d.file_percent)
            Thread(target=ftp_sock.send_file, args=(list_file[1], list_file[0], self.d.file_percent,)).start()


    def set_value_upload(self, value):
        self.upload_bar.setValue(value)

class Communicate(QObject):
    print_chat = pyqtSignal(int, str)
    print_info = pyqtSignal(dict)
    file_percent = pyqtSignal(int)

class changePwdWindown(QWidget):
    def __init__(self):
        super(changePwdWindown, self).__init__()
        self.title = 'Change password'
        self.left = 500
        self.top = 300
        self.width = 300
        self.height = 100
        self.initUI()
        self.show()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        form = QFormLayout()

        cur_pwd = QLabel("Old Password")
        self.cur_pwdEntry = QLineEdit()
        self.cur_pwdEntry.setEchoMode(QLineEdit.Password)
        form.addRow(cur_pwd, self.cur_pwdEntry)

        newpwd = QLabel("New password")
        self.newpwd_entry = QLineEdit()
        self.newpwd_entry.setEchoMode(QLineEdit.Password)
        form.addRow(newpwd, self.newpwd_entry)

        newpwd_verify = QLabel("Verify password")
        self.newpwd_verify_entry = QLineEdit()
        self.newpwd_verify_entry.setEchoMode(QLineEdit.Password)
        form.addRow(newpwd_verify, self.newpwd_verify_entry)

        btn = QPushButton("Change")
        form.addRow(btn)
        btn.clicked.connect(self.processing)
        self.mainLayout.addLayout(form)
        self.setLayout(self.mainLayout)

    def processing(self):
        global client
        global session_id
        newpwd = self.newpwd_entry.text()
        newpwd2 = self.newpwd_verify_entry.text()
        ########### checking #####################
        if not newpwd or not newpwd2 or not self.cur_pwdEntry.text():
            QMessageBox.information(self, "Notification", "Do not empty!!!!",
                                    QMessageBox.Ok, QMessageBox.Ok)
        elif newpwd != newpwd2:
            QMessageBox.information(self, "Notification", "new password doesn't match confirm password",
                                    QMessageBox.Ok, QMessageBox.Ok)
        elif client.password != self.cur_pwdEntry.text():
            QMessageBox.information(self, "Notification", "Old password is wrong!!!!",
                                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            changeJSON = json.dumps({"pwd": client.password, "new_pwd": newpwd,
                                     "action": "change_pwd", "session_id": session_id})
            QMessageBox.information(self, "Notification", "Successful!!!!",
                                    QMessageBox.Ok, QMessageBox.Ok)
            # client.s.send(changeJSON.encode())
            json_util.send(changeJSON, client.s)


class myProfileWindow(QListWidget):
    def __init__(self):
        super(myProfileWindow, self).__init__()
        self.title = 'My Profile'
        self.left = 500
        self.top = 300
        self.width = 300
        self.height = 100
        self.initUI()
        self.show()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('image/chat.png'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        form = QFormLayout()


##############start##############
if __name__ == '__main__':
    client = Client()
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = startWindow()
    os._exit(app.exec_())
