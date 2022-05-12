import os
import socket
import string
import threading
import time

import paramiko as paramiko
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from initial.ssh_handler import ShellHandler
from initial.utility import *


class BehaviourManager:
    def __init__(self, beh_depend_status, window):
        self.window = window

        self.beh_depend_status = beh_depend_status

        self._beh_status = False

        self.file_list = []
        self._selected_item = None
        self._script_dir_path = fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage"
        self.script_dir = QDir(self._script_dir_path)
        if not self.script_dir.exists():
            self.script_dir.mkpath(self._script_dir_path)

    """
    GETTERS & SETTERS
    """

    @property
    def script_status(self) -> bool:
        return self._beh_status

    @script_status.setter
    def script_status(self, value: bool):
        self.window.findChild(QPushButton, "startScript").setEnabled(not value)
        self.window.findChild(QPushButton, "stopScript").setEnabled(value)
        self._beh_status = value

    @property
    def selected_item(self) -> QListWidgetItem:
        return self._selected_item

    @selected_item.setter
    def selected_item(self, item: QListWidgetItem):
        self._selected_item = item

    def new_item_selected(self) -> QListWidgetItem:
        self.selected_item = [
            res for res in self.window.findChild(QListWidget, "pyAvailableList").findItems(".py", Qt.MatchContains)
            if res.isSelected()
        ][0]
        return self.selected_item

    def update_script_table(self):
        self.script_dir = QDir(fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage")
        self.script_dir.entryList()
        # QListWidget.clear
        self.window.findChild(QListWidget, "pyAvailableList").clear()
        self.file_list = self.script_dir.entryList(["*.py", QDir.Files])
        # self.window.findChild(QTableWidget, "pptxAvailableTable").setRowCount(len(self.file_list))
        for fileName, fileNum in zip(self.file_list, range(len(self.file_list))):
            # print(fileName, fileNum, self.file_list)
            self.window.findChild(QListWidget, "pyAvailableList").addItem(QListWidgetItem(fileName))
            # self.window.findChild(QListWidget, "pptxAvailableTable").
            # QListWidget.sil
            # self.window.findChild(QListWidget, "pptxAvailableTable").findItems(fileName, Qt.MatchContains)[0].clicked.connect(lambda: print(fileName))
            # QListWidgetItem.
            # self.window.findChild(QTableWidget, "pptxAvailableTable").setItem(fileNum, 0, QTableWidgetItem(fileName))
            # QListWidgetItem.

    """
    TRIGGERS
    """

    # def set_file_path(self, label: QLabel):
    #     filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    #     label.setText(filepath)

    def setup_triggers(self):
        self.window.findChild(QToolButton, "scriptFindFile").clicked.connect(
            lambda: set_file_path(self.window.findChild(QLineEdit, "selScriptPathInp"))
        )
        self.window.findChild(QLineEdit, "selScriptPathInp").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selScriptPathInp"),
                                          self.window.findChild(QPushButton, "scriptAddButton"))
        )
        self.window.findChild(QPushButton, "scriptAddButton").clicked.connect(lambda: self.add_script())
        self.window.findChild(QListWidget, "pyAvailableList").clicked.connect(
            lambda: self.select_script(self.new_item_selected())
        )

        """
        .....
        """

        self.window.findChild(QLineEdit, "selScriptOutLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selScriptOutLine"),
                                          self.window.findChild(QPushButton, "startScript")))
        self.window.findChild(QLineEdit, "selScriptOutLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selScriptOutLine"),
                                          self.window.findChild(QPushButton, "delScriptButton")))

        self.window.findChild(QPushButton, "startScript").clicked.connect(
            lambda: self.start_script())
        self.window.findChild(QPushButton, "stopScript").clicked.connect(
            lambda: self.stop_script())
        self.window.findChild(QPushButton, "delScriptButton").clicked.connect(
            lambda: self.delete_cur_script())

    def start_script(self):
        self.script_status = True

    def stop_script(self):
        self.script_status = False

    def add_script(self):
        add_file_to_storage(self.window.findChild(QLineEdit, "selScriptPathInp").text())
        self.update_script_table()

    def delete_cur_script(self):
        self.script_dir.remove(self.selected_item.text())
        self.update_script_table()

    def select_script(self, selected_item: QListWidgetItem):
        self.window.findChild(QLineEdit, "selScriptOutLine").setText(selected_item.text())

    """
    DESIGN
    """

    def script_dependency(self, status: bool):
        pass

    def make_shiny(self):
        self.setup_table()
        # while self.inf_status:
        #     time.sleep(1)

    def setup_table(self):
        self.update_script_table()
        # QListWidget.addItem(self.window.findChild(QPushButton, "pptxAddButton"))
        # self.window.findChild(QListWidget, "pptxAvailableTable").addItem("123")
        # self.window.findChild(QTableWidget, "pptxAvailableTable").setColumnWidth(1, 118)
        # self.window.findChild(QTableWidget, "pptxAvailableTable").setItem(1,1,QTableWidgetItem("зызызыз"))
