import socket
import string

import paramiko as paramiko
from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit


class RobotConnector:
    def __init__(self, window):
        self.window = window
        self._ip = None
        self._user = None
        self._password = None
        self._connection_status = None

        self._connection_handler = None

        self.setup_triggers()

        pass

    """
    GETTERS \ SETTERS
    """

    @property
    def ip(self) -> string:
        return self._ip

    @ip.setter
    def ip(self, value: string):
        self._ip = value

    @property
    def user(self) -> string:
        return self._user

    @user.setter
    def user(self, value: string):
        self._user = value

    @property
    def password(self) -> string:
        return self._password

    @password.setter
    def password(self, value: string):
        self._password = value

    @property
    def connection_status(self) -> string:
        return self._connection_status

    @connection_status.setter
    def connection_status(self, value: string):
        self._connection_status = value

    @property
    def connection_handler(self):
        return self._connection_handler

    @connection_handler.setter
    def connection_handler(self, func):
        self._connection_handler = func

    """
    connection func
    """

    def create_connection_handler(self):
        self.get_connection_fields()
        if "" not in [self.ip, self.user, self.password]:
            try:
                self.window.findChild(QLineEdit, "robConStatusOut").setText(self.create_handler())
            except socket.gaierror:
                self.window.findChild(QLineEdit, "robConStatusOut").setText("ERROR")
            return
        self.window.findChild(QLineEdit, "robConStatusOut").setText("ERROR")

    def setup_triggers(self):
        self.window.findChild(QPushButton, "robConConnectButton").clicked.connect(self.create_connection_handler)
        self.window.findChild(QLineEdit, "robotLineInp").returnPressed.connect(self.robot_console_worker)

    def robot_console_worker(self):
        com_handler = self.window.findChild(QLineEdit, "robotLineInp")
        self.window.findChild(QTextEdit, "robotTextOut").append(self.connection_handler(com_handler.text()))
        com_handler.clear()


    def get_connection_fields(self):
        ip_handler = self.window.findChild(QLineEdit, "robConIpInp")
        self.ip = ip_handler.text()

        user_handler = self.window.findChild(QLineEdit, "robConUserInp")
        self.user = user_handler.text()
        password_handler = self.window.findChild(QLineEdit, "robConPassInp")
        self.password = password_handler.text()
        print(ip_handler.text())
        # ip_handler.clear()

    def create_handler(self) -> string:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, 22, self.user, self.password)
        self.connection_handler = lambda v: f">{v}\n" + "".join([j for i in ssh.exec_command(v)[1:] if i != "" for j in i.readlines()])
        self.connection_status = "CONNECTED"
        return self.connection_status

# self.ip
