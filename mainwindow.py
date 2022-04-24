# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

import PySide6
from PySide6 import *
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from initial.main_window_handler import MainWindowHandler


def make_shiny_and_connect_all(window: QWidget) -> MainWindowHandler:
    handler = MainWindowHandler(window)
    handler.make_shiny()
    handler.connect()
    return handler


if __name__ == "__main__":
    app = QApplication([])
    path = os.fspath(Path(__file__).resolve().parent / "form.ui")
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file, None)

    windowHandler = make_shiny_and_connect_all(window)
    # windowHandler.window.findChild(PySide6.QtWidgets.QLineEdit, "robotLineEdit").setEnabled(True)
    # window.findChild(PySide6.QtWidgets.QLineEdit, "robotLineEdit").returnPressed.connect(lambda: print("hihihaha"))
    # window.main.returnPressed.connect(lambda :print("hihihaha"))
    # window.findChild(PySide6.QtWidgets.QListWidget, "listWidget").addItem(QListWidgetItem("hihihaha"))

    window.show()
    sys.exit(app.exec())
