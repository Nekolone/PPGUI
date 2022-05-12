import os
import socket
import string
import threading
import time

import paramiko as paramiko
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from initial.ssh_handler import ShellHandler
from initial.utility import *


# QTextEdit.cursorForPosition().currentFrame()


class SlideDesigner:
    def __init__(self, window):
        self.window = window

        self._cur_pointer_pos = None

    """
    GETTERS & SETTERS
    """

    @property
    def cur_pointer_pos(self) -> QTextFrame:
        return self._cur_pointer_pos

    @cur_pointer_pos.setter
    def cur_pointer_pos(self, value: QTextFrame):
        self._cur_pointer_pos = value

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

        QTextEdit.cursorForPosition().currentFrame()

    def setup_table(self):
        self.update_script_table()
        # QListWidget.addItem(self.window.findChild(QPushButton, "pptxAddButton"))
        # self.window.findChild(QListWidget, "pptxAvailableTable").addItem("123")
        # self.window.findChild(QTableWidget, "pptxAvailableTable").setColumnWidth(1, 118)
        # self.window.findChild(QTableWidget, "pptxAvailableTable").setItem(1,1,QTableWidgetItem("зызызыз"))
