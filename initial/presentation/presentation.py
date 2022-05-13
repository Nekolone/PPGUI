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


class PresentationConnector:
    def __init__(self, pres_depend_status, window):
        self.window = window

        self.pres_depend_status = pres_depend_status

        self._pres_status = False

        self._inter_state = False

        self.file_list = []
        self._selected_item = None
        self.pres_dir_path = fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage"
        self.pres_dir = QDir(self.pres_dir_path)
        if not self.pres_dir.exists():
            self.pres_dir.mkpath(self.pres_dir_path)

    """
    GETTERS & SETTERS
    """

    @property
    def pres_status(self) -> bool:
        return self._pres_status

    @pres_status.setter
    def pres_status(self, value: bool):
        self.window.findChild(QPushButton, "startPres").setEnabled(not value)
        self.window.findChild(QPushButton, "stopPres").setEnabled(value)
        self.pres_depend_status(value)
        self._pres_status = value

    @property
    def selected_item(self) -> QListWidgetItem:
        return self._selected_item

    @selected_item.setter
    def selected_item(self, item: QListWidgetItem):
        self._selected_item = item

    def new_item_selected(self) -> QListWidgetItem:
        self.selected_item = [
            res for res in self.window.findChild(QListWidget, "pptxAvailableTable").findItems(".pptx", Qt.MatchContains)
            if res.isSelected()
        ][0]
        return self.selected_item

    def update_pres_table(self):
        self.pres_dir = QDir(fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage")
        self.pres_dir.entryList()
        self.window.findChild(QListWidget, "pptxAvailableTable").clear()
        self.file_list = self.pres_dir.entryList(["*.pptx", QDir.Files])
        for fileName, fileNum in zip(self.file_list, range(len(self.file_list))):
            self.window.findChild(QListWidget, "pptxAvailableTable").addItem(QListWidgetItem(fileName))

    @property
    def inter_state(self):
        return self._inter_state

    @inter_state.setter
    def inter_state(self, value):
        self._inter_state = value

    def validate_cur_pres(self):
        self.window.findChild(QLineEdit, "valStatusOutLine").setText(".")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText("..")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText("...")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText("....")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText(".....")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText("......")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText(".......")
        time.sleep(0.3)
        self.window.findChild(QLineEdit, "valStatusOutLine").setText("Success")

    """
    TRIGGERS
    """

    def setup_triggers(self):
        self.window.findChild(QToolButton, "pptxFindFile").clicked.connect(
            lambda: set_file_path(self.window.findChild(QLineEdit, "pptxPathLine"))
        )
        self.window.findChild(QLineEdit, "pptxPathLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "pptxPathLine"),
                                          self.window.findChild(QPushButton, "pptxAddButton"))
        )
        self.window.findChild(QPushButton, "pptxAddButton").clicked.connect(lambda: self.add_presentation())
        self.window.findChild(QListWidget, "pptxAvailableTable").clicked.connect(
            lambda: self.select_presentation(self.new_item_selected())
        )

        self.window.findChild(QCheckBox, "intConnection").clicked.connect(lambda: self.check_int_state())
        self.window.findChild(QLineEdit, "selPresOutLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selPresOutLine"),
                                          self.window.findChild(QPushButton, "startPres")))
        self.window.findChild(QLineEdit, "selPresOutLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selPresOutLine"),
                                          self.window.findChild(QPushButton, "delPresCheckButton")))

        self.window.findChild(QPushButton, "valPresCheckButton").clicked.connect(
            lambda: threading.Thread(target=self.validate_cur_pres, args=()).start())
        self.window.findChild(QPushButton, "startPres").clicked.connect(
            lambda: self.start_presentation())
        self.window.findChild(QPushButton, "stopPres").clicked.connect(
            lambda: self.stop_presentation())
        self.window.findChild(QPushButton, "delPresCheckButton").clicked.connect(
            lambda: self.delete_cur_pres())

    def start_presentation(self):
        self.pres_status = True

    def stop_presentation(self):
        self.pres_status = False

    def add_presentation(self):
        add_file_to_storage(self.window.findChild(QLineEdit, "pptxPathLine").text())
        self.update_pres_table()

    def delete_cur_pres(self):
        self.pres_dir.remove(self.selected_item.text())
        self.update_pres_table()

    def select_presentation(self, selected_item: QListWidgetItem):
        self.window.findChild(QLineEdit, "selPresOutLine").setText(selected_item.text())
        self.window.findChild(QPushButton, "valPresCheckButton").setEnabled(True)
        self.window.findChild(QLineEdit, "valStatusOutLine").setEnabled(True)
        self.window.findChild(QLineEdit, "valStatusOutLine").clear()

    def check_int_state(self):
        self.inter_state = self.window.findChild(QCheckBox, "intConnection").isChecked()

    """
    DESIGN
    """

    def presentation_dependency(self, status: bool):
        pass

    def make_shiny(self):
        self.setup_table()

    def setup_table(self):
        self.update_pres_table()
