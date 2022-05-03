import socket
import string
import threading
import time

import paramiko as paramiko
from PySide6.QtWidgets import *

from initial.ssh_handler import ShellHandler
from initial.utility import activate_if_not_blank


class PresentationConnector:
    def __init__(self, pres_depend_status, window):
        self.window = window

        self.pres_depend_status = pres_depend_status

        self._pres_status = False

        # self.present_depend_status = present_depend_status

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
        self._pres_status = value


    """
    TRIGGERS
    """

    def find_pptx(self):
        pass

    def set_file_path(self, label: QLabel):
        filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
        label.setText(filepath)

    def setup_triggers(self):
        self.window.findChild(QToolButton, "pptxFindFile").clicked.connect(
            lambda: self.set_file_path(self.window.findChild(QLineEdit, "pptxPathLine")))
        self.window.findChild(QLineEdit, "pptxPathLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "pptxPathLine"),
                                          self.window.findChild(QPushButton, "pptxAddButton")))
        # self.window.findChild(QPushButton, "pptxAddButton").clkiced.connect(
        #
        # )

        """
        .....
        """

        self.window.findChild(QLineEdit, "selPresOutLine").textChanged.connect(
            lambda: activate_if_not_blank(self.window.findChild(QLineEdit, "selPresOutLine"),
                                          self.window.findChild(QPushButton, "startPres")))

        self.window.findChild(QPushButton, "startPres").clicked.connect(
            lambda: self.start_presentation())
        self.window.findChild(QPushButton, "stopPres").clicked.connect(
            lambda: self.stop_presentation())

    def start_presentation(self):
        self.pres_status = True

    def stop_presentation(self):
        self.pres_status = False

    """
    DESIGN
    """

    def presentation_dependency(self, status: bool):
        pass

    def make_shiny(self):
        pass
        # while self.inf_status:
        #     time.sleep(1)
