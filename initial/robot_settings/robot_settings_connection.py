import socket
import string
import threading
import time

import paramiko as paramiko
from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit, QGroupBox, QWidget

from initial.ssh_handler import ShellHandler


class RobotConnector:
    def __init__(self, conn_depend_status, window):
        self.inf_status = True
        self.window = window
        self._ip = None
        self._user = None
        self._password = None
        self._connection_status = None
        # self.stdin = None
        # self.stdout = None
        # self.stderr = None
        self.ssh_conn = None

        self.conn_depend_status = conn_depend_status

        self._connection_handler = None

    """
    GETTERS & SETTERS
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
        self.conn_depend_status(value == "CONNECTED")
        self._connection_status = value

    @property
    def connection_handler(self):
        return self._connection_handler

    @connection_handler.setter
    def connection_handler(self, func):
        self._connection_handler = func

    """
    SSH CONNECTION
    """

    def create_connection_handler(self):
        self.get_connection_fields()
        if "" not in [self.ip, self.user, self.password]:
            try:
                self.window.findChild(QLineEdit, "robConStatusOut").setText(self.create_handler())
            except socket.gaierror:
                self.window.findChild(QLineEdit, "robConStatusOut").setText("DISCONNECTED")
            return
        self.window.findChild(QLineEdit, "robConStatusOut").setText("DISCONNECTED")

    def get_connection_fields(self):
        ip_handler = self.window.findChild(QLineEdit, "robConIpInp")
        self.ip = ip_handler.text()

        user_handler = self.window.findChild(QLineEdit, "robConUserInp")
        self.user = user_handler.text()

        password_handler = self.window.findChild(QLineEdit, "robConPassInp")
        self.password = password_handler.text()
        print(ip_handler.text())

    """
    TRIGGERS
    """

    def setup_triggers(self):
        self.window.findChild(QPushButton, "robSysRebootButton").clicked.connect(
            lambda: self.connection_handler("touch /home/dummy/test_file"))
        self.window.findChild(QPushButton, "robConConnectButton").clicked.connect(
            lambda: threading.Thread(target=self.create_connection_handler, args=()).start())
        self.window.findChild(QLineEdit, "robotLineInp").returnPressed.connect(self.robot_console_worker)

    """
    CONSOLE REALISATION
    """

    def robot_console_worker(self):
        com_handler = self.window.findChild(QLineEdit, "robotLineInp")
        self.window.findChild(QTextEdit, "robotTextOut").append(self.connection_handler(com_handler.text()))
        com_handler.clear()
        # ip_handler.clear()

    def create_handler(self) -> string:
        try:
            self.ssh_conn = ShellHandler(self.ip, self.user, self.password)
            self.connection_handler = lambda v: self.exec_command(v)
            self.connection_status = "CONNECTED"
        except TimeoutError as e:
            self.connection_status = "DISCONNECTED"
            self.window.findChild(QTextEdit, "robotTextOut").append(e.strerror)
        return self.connection_status

    def exec_command(self, command) -> string:
        try:
            return f">{command}\n" + "".join(["".join(i) for i in self.ssh_conn.execute(command)[1:] if i !=""])
        except (ConnectionResetError, paramiko.SSHException, socket.error):
            self.connection_status = "DISCONNECTED"

    """
    DESIGN
    """

    def connection_dependency(self, status: bool):

        [c.setEnabled(status) for c in self.window.findChild(QGroupBox, "robSysGroupBox").children()]
        [c.setEnabled(status) for c in self.window.findChild(QWidget, "robotTabBot").children()]

        self.window.findChild(QPushButton, "robConConnectButton").setEnabled(not status)
        self.window.findChild(QLineEdit, "robConStatusOut").setText("CONNECTED" if status else "DISCONNECTED")

    def make_shiny(self):
        pass
        # while self.inf_status:
        #     time.sleep(1)
