import ctypes
import sys
import threading

from PySide6.QtCore import QProcess, Qt
from PySide6.QtWidgets import QPushButton, QListWidgetItem, QListWidget

from initial.utility import *

CP_console = f"cp{ctypes.cdll.kernel32.GetConsoleOutputCP()}"


class BehaviourManager:
    def __init__(self, beh_depend_status, window, robot_con):
        self.window = window

        self.robot_con = robot_con

        self.beh_depend_status = beh_depend_status

        self._beh_status = False

        self.beh_list = []
        self._selected_item = None

        self.beh_proc = QProcess()

        # self._script_dir_path = fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage"
        # self.script_dir = QDir(self._script_dir_path)
        # if not self.script_dir.exists():
        #     self.script_dir.mkpath(self._script_dir_path)

    """
    GETTERS & SETTERS
    """

    @property
    def beh_status(self) -> bool:
        return self._beh_status

    @beh_status.setter
    def beh_status(self, value: bool):
        self.window.findChild(QPushButton, "startBeh").setEnabled(not value)
        self.window.findChild(QPushButton, "stopBeh").setEnabled(value)
        self._beh_status = value

    @property
    def selected_item(self) -> QListWidgetItem:
        return self._selected_item

    @selected_item.setter
    def selected_item(self, item: QListWidgetItem):
        self._selected_item = item

    def new_item_selected(self) -> QListWidgetItem:
        self.selected_item = [
            res for res in self.window.findChild(QListWidget, "benManTable").findItems("", Qt.MatchContains)
            if res.isSelected()
        ][0]
        return self.selected_item

    def test(self, texts):
        print("тут")
        print(texts)

    def dataReady(self):
        # cursor = self.output.textCursor()
        # cursor.movePosition(cursor.MoveOperation.End)

        # Here we have to decode the QByteArray
        print("123")
        res = str(self.beh_proc.readAll().data().decode(CP_console)).split("\r\n")
        print(res)
        self.window.findChild(QListWidget, "benManTable").clear()
        for r in res[1:]:
            self.window.findChild(QListWidget, "benManTable").addItem(QListWidgetItem(r))
        # print(str(self.beh_proc.readAllStandardError().data().decode(CP_console)))
        # print(str(self.beh_proc.readAllStandardOutput().data().decode(CP_console)))
        # self.output.ensureCursorVisible()

    def update_beh_table(self):
        # print(rf'{os.getcwd()}\behaviours.exe')
        # self.beh_proc.readyReadStandardError.connect(self.dataReady)
        self.beh_proc.readyRead.connect(self.dataReady)
        self.beh_proc.readyReadStandardError.connect(lambda: print("dfd"))
        self.beh_proc.start(rf'{sys._MEIPASS}\behaviours.exe', ['--ip', f'{self.robot_con.ip}'])

    # f"""import qi; s = qi.Session(); s.connect("tcp://localhost:9559"); b = s.service("ALBehaviorManager"); b.startBehavior("{}")"""
    """
    TRIGGERS
    """

    # def set_file_path(self, label: QLabel):
    #     filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    #     label.setText(filepath)

    def setup_triggers(self):
        self.window.findChild(QListWidget, "benManTable").clicked.connect(
            lambda: self.select_beh(self.new_item_selected())
        )

        self.window.findChild(QPushButton, "startBeh").clicked.connect(
            lambda: self.start_beh())
        self.window.findChild(QPushButton, "stopBeh").clicked.connect(
            lambda: self.stop_beh())

    def start_beh(self):
        start_beh_on_nao = self.window.findChild(QLineEdit, "selBehOutLine").text()
        text = self.window.findChild(QLineEdit, "selBehOutLine").text()
        command = """python -c \"import qi; s = qi.Session(); s.connect('tcp://localhost:9559'); b = s.service('ALBehaviorManager'); b.startBehavior('{}')\"""".format(
            text)
        print(text)
        print(command)
        threading.Thread(target=self.robot_con.connection_handler, args=(command,)).start()
        # self.robot_con.ssh_conn.execute(command)
        # self.update_beh_table()
        # self.
        # self.beh_status = True

    def stop_beh(self):
        self.update_beh_table()
        # self.beh_status = False
        # self.beh_proc.kill()

    def select_beh(self, selected_item: QListWidgetItem):
        self.window.findChild(QLineEdit, "selBehOutLine").setText(selected_item.text())

    """
    DESIGN
    """

    def script_dependency(self, status: bool):
        pass

    def make_shiny(self):
        pass
        # self.setup_table()
        # while self.inf_status:
        #     time.sleep(1)

    # def setup_table(self):
    #     pass
    # self.update_script_table()
    # QListWidget.addItem(self.window.findChild(QPushButton, "pptxAddButton"))
    # self.window.findChild(QListWidget, "pptxAvailableTable").addItem("123")
    # self.window.findChild(QTableWidget, "pptxAvailableTable").setColumnWidth(1, 118)
    # self.window.findChild(QTableWidget, "pptxAvailableTable").setItem(1,1,QTableWidgetItem("зызызыз"))
