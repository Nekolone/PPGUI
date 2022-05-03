from PySide6.QtWidgets import *


def activate_if_not_blank(label: QLineEdit, target: QLabel):
    set_enabled_status(not label.text() == "", target)


def set_enabled_status(status, target: QLabel):
    target.setEnabled(status)
