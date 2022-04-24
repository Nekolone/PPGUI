from PySide6.QtWidgets import QWidget

from initial.robot_settings.robot_settings_connection import RobotConnector


class MainWindowHandler:
    def __init__(self, window: QWidget):
        self.robot_connection = RobotConnector(window)
        self.connection_handler = self.robot_connection.connection_handler
        self.window = window

    def make_shiny(self):
        pass

    def connect(self):

        pass
