import socket
import string
import threading

import paramiko as paramiko
from PySide6.QtWidgets import QLineEdit, QPushButton, QTextEdit, QGroupBox, QWidget

from initial.ssh_handler import SecureShellHandler


class RobotConnector:
    def __init__(self, conn_depend_status, window):
        self.window = window
        self._ip: string = None
        self._user: string = None
        self._password: string = None

        self._connection_status: string = "DISCONNECTED"
        self._thread_status: bool = False

        self.stat_updater_thread: threading = threading.Thread(target=self.update_robot_stats, args=())
        # self.stdin = None
        # self.stdout = None
        # self.stderr = None
        self.ssh_conn = None

        self.conn_depend_status = conn_depend_status

        self._connection_handler = None
        self._connection_handler_single_com = None

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

    @property
    def connection_handler_single_com(self):
        return self._connection_handler_single_com

    @connection_handler_single_com.setter
    def connection_handler_single_com(self, func):
        self._connection_handler_single_com = func

    @property
    def thread_status(self) -> bool:
        return self._thread_status

    @thread_status.setter
    def thread_status(self, value: bool):
        self._thread_status = value

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
            lambda: threading.Thread(target=self.connection_handler, args=("reboot",)).start())
        self.window.findChild(QPushButton, "robConConnectButton").clicked.connect(
            lambda: threading.Thread(target=self.create_connection_handler, args=()).start())
        self.window.findChild(QLineEdit, "robotLineInp").returnPressed.connect(self.robot_console_worker)
        # QCloseEvent
        # self.thread_status

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
            self.ssh_conn = SecureShellHandler(self.ip, self.user, self.password)
            self.connection_handler = lambda v: self.exec_command(v)
            self.connection_handler_single_com = lambda v: self.exec_single_command(v)
            self.connection_status = "CONNECTED"
        except TimeoutError as e:
            self.connection_status = "DISCONNECTED"
            self.window.findChild(QTextEdit, "robotTextOut").append(e.strerror)
        return self.connection_status

    def exec_command(self, command) -> string:
        try:
            return f">{command}\n" + "".join(["".join(i) for i in self.ssh_conn.execute(command)[1:] if i != ""])
        except (ConnectionResetError, paramiko.SSHException, socket.error):
            self.connection_status = "DISCONNECTED"

    def exec_single_command(self, command) -> string:
        try:
            return "".join([j for i in self.ssh_conn.ssh.exec_command(command)[1:] if i != "" for j in i.readlines()])
        except (ConnectionResetError, paramiko.SSHException, socket.error):
            self.connection_status = "DISCONNECTED"

    """
    ROBOT USAGE
    """

    def update_robot_stats(self):
        while self.thread_status:
            self.window.findChild(QLineEdit, "robSysCpuOut").setText(self.connection_handler_single_com(
                r"""top -b -n2 -p 1 | fgrep "Cpu(s)" | tail -1 | awk -F'id,' -v prefix="$prefix" '{ split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf "%s%.1f%%\n", prefix, 100 - v }'"""
            ))
            self.window.findChild(QLineEdit, "robSysRamOut").setText(self.connection_handler_single_com(
                r"""free -m | grep "Mem" | awk '{printf("%dM / %dM\n", $3, $2)}'"""
            ))
            self.window.findChild(QLineEdit, "robSysUptimeOut").setText(self.connection_handler_single_com(
                """awk '{print int(($1/3600)/24)"d:"int(($1/3600)%60)"h:"int(($1%3600)/60)"m:"int($1%60)"s"}' /proc/uptime"""
            ))

    """
    DESIGN
    """

    def connection_dependency(self, status: bool):

        [c.setEnabled(status) for c in self.window.findChild(QGroupBox, "robSysGroupBox").children()]
        [c.setEnabled(status) for c in self.window.findChild(QWidget, "robotTabBot").children()]

        self.window.findChild(QPushButton, "robConConnectButton").setEnabled(not status)
        self.window.findChild(QLineEdit, "robConStatusOut").setText("CONNECTED" if status else "DISCONNECTED")

        if status:
            if not self.stat_updater_thread.is_alive():
                self.thread_status = True
                self.stat_updater_thread.start()
            return
        self.thread_status = False

    def make_shiny(self):
        pass
        # while self.inf_status:
        #     time.sleep(1)
