import os
import shutil
import string

from PySide6.QtWidgets import *


def activate_if_not_blank(label: QLineEdit, target: QLabel):
    set_enabled_status(not label.text() == "", target)


def set_enabled_status(status, target: QLabel):
    target.setEnabled(status)


def add_file_to_storage(filepath: string):
    try:
        os.mkdir(filepath)
    except FileExistsError:
        pass
    shutil.copy(filepath, fr"{os.environ['USERPROFILE']}\Documents\NaoGuiShellStorage")
