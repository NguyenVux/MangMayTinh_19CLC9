import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

font = QFont("Arial", 10, 80)


class startWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Test'
        self.left = 500
        self.top = 300
        self.width = 300
        self.height = 150
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
        hbox_top=QHBoxLayout()
        hbox_mid = QHBoxLayout()
        hbox_down = QHBoxLayout()

        p=QPixmap('image/cloud-computing.png')
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
        port_input.returnPressed.connect(lambda: self.connectServer(host_input.text(), port_input.text()))

        quit_btn = QPushButton("Quit")
        connect_btn = QPushButton("Connect")
        hbox_down.addStretch()
        hbox_down.addWidget(quit_btn)
        hbox_down.addWidget(connect_btn)
        connect_form.addRow(hbox_down)

        quit_btn.clicked.connect(self.exitApp)

        connect_btn.clicked.connect(lambda: self.connectServer(host_input.text(), port_input.text()))
        ########Dislay to screen##########
        self.mainLayout.addLayout(connect_form)
        self.setLayout(self.mainLayout)

    def exitApp(self):
        notify = QMessageBox.information(self, "Notification", "Are you want to exit?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if notify == QMessageBox.Yes:
            sys.exit()

    def connectServer(self, host, port):
        if host == "" or port == "":
            QMessageBox.information(self, "Warning!", "Do not empty!!!!", QMessageBox.Ok, QMessageBox.Ok)
        else:
            ##########connect##########

            ##########login###########
            pass

class login(QWidget):
    pass


##############start##############
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    window = startWindow()
    sys.exit(app.exec_())
