from PySide6.QtWidgets import QWidget

from initial.robot_settings.robot_settings_connection import RobotConnector


class MainWindowHandler:
    def __init__(self, window: QWidget):
        self.robot_connection = RobotConnector(self.set_obj_status_by_connection, window)
        self.connection_handler = self.robot_connection.connection_handler
        self.window = window

    def make_shiny(self):
        self.robot_connection.make_shiny()
        pass

    def connect(self):
        self.robot_connection.setup_triggers()
        pass

    def set_obj_status_by_connection(self, status: bool):
        self.robot_connection.connection_dependency(status)

