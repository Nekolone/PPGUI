from PySide6.QtWidgets import QWidget

from initial.presentation.presentation import PresentationConnector
from initial.robot_settings.robot_settings import RobotConnector


class MainWindowHandler:
    def __init__(self, window: QWidget):
        self.window = window

        self.robot_connection = RobotConnector(self.set_connection_status_dependencies, window)
        self.connection_handler = self.robot_connection.connection_handler

        self.presentation_connection = PresentationConnector(self.set_presentation_status_dependencies, window)

        self.thread_list = []

        self._connection_status = False
        self._presentation_status = False

    """
    GETTERS & SETTERS
    """

    @property
    def connection_status(self) -> bool:
        return self._connection_status

    @connection_status.setter
    def connection_status(self, value: bool):
        self._connection_status = value

    @property
    def presentation_status(self) -> bool:
        return self._presentation_status

    @presentation_status.setter
    def presentation_status(self, value: bool):

        self._presentation_status = value

    """
    IMPORTANT THINGS
    """

    def make_shiny(self):
        self.robot_connection.make_shiny()
        self.presentation_connection.make_shiny()
        pass

    def connect(self):
        self.robot_connection.setup_triggers()
        self.presentation_connection.setup_triggers()
        pass

    """
    DEPENDENCIES
    """

    def set_connection_status_dependencies(self, status: bool):
        self.connection_status = status
        self.robot_connection.connection_dependency(status)

    def set_presentation_status_dependencies(self, status: bool):
        self.presentation_status = status
