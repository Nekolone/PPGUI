# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget

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

    window.show()
    sys.exit(app.exec())
