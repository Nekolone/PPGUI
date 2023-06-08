import sys

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import QWidget

from initial.behaviour_manager.behaviour_manager import BehaviourManager, CP_console
from initial.presentation.presentation import PresentationConnector
from initial.robot_settings.robot_settings import RobotConnector
from initial.script_manager.script_manager import ScriptManager
from initial.slide_designer.slide_designer import SlideDesigner
from initial.utility import *


class MainWindowHandler:
    def __init__(self, window: QWidget):
        self.window = window

        self.robot_connection = RobotConnector(self.set_connection_status_dependencies, window)
        self.connection_handler = self.robot_connection.connection_handler

        self.presentation_connection = PresentationConnector(self.set_presentation_status_dependencies, window)

        self.script_manager = ScriptManager(self.set_script_status_dependencies, window)

        self.behaviour_manager = BehaviourManager(self.get_beh_list, window, self.robot_connection)

        self.slide_manager = SlideDesigner(window)

        self.p = QProcess()
        self.p.finished.connect(lambda: self.presentation_stopped())

        self.sp = QProcess()
        # self.sp.finished.connect(lambda: self.presentation_stopped())

        self.thread_list = []

        self._connection_status = False
        self._presentation_status = False
        self._script_status = False

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
        if value:
            self.start_presentation()
        else:
            self.stop_presentation()
        self._presentation_status = value

    @property
    def script_status(self) -> bool:
        return self._script_status

    @script_status.setter
    def script_status(self, value: bool):
        if value:
            self.start_script()
        else:
            self.stop_script()
        self._script_status = value

    """
    IMPORTANT THINGS
    """

    def make_shiny(self):
        self.robot_connection.make_shiny()
        self.presentation_connection.make_shiny()
        self.script_manager.make_shiny()
        # self.script_manager.make_shiny()

    def connect(self):
        self.robot_connection.setup_triggers()
        self.presentation_connection.setup_triggers()
        self.script_manager.setup_triggers()
        self.behaviour_manager.setup_triggers()
        self.slide_manager.setup_triggers()

    """
    DEPENDENCIES
    """

    def set_connection_status_dependencies(self, status: bool):
        self.connection_status = status
        self.robot_connection.connection_dependency(status)
        # self.behaviour_manager.update_beh_table()

    def set_presentation_status_dependencies(self, status: bool):
        self.presentation_status = status

    def set_script_status_dependencies(self, status: bool):
        self.script_status = status

    def get_beh_list(self) -> QProcess:
        beh_proc = QProcess()
        beh_proc.setProgram(f"{sys._MEIPASS}\\behaviours.exe")
        beh_proc.setArguments(["--ip", self.robot_connection.ip])
        return beh_proc

    """
    CONTROLLERS
    """

    def start_presentation(self):
        self.p.setProgram(rf"{sys._MEIPASS}\naopptx.exe")
        args = ["--pr", self.presentation_connection.pres_dir_path + "\\" +
                self.presentation_connection.selected_item.text(),
                "--ip", self.robot_connection.ip]
        if not self.presentation_connection.inter_state:
            args.append("--no-inet")
        print(args)
        self.p.setArguments(args)
        self.p.start()

    def stop_presentation(self):
        self.p.kill()
        pass

    def presentation_stopped(self):
        self.presentation_connection.pres_status = False

    def dataReady(self):
        print(str(self.sp.readAll().data().decode(CP_console)))

    def start_script(self):

        # self.sp.setProgram("python3")
        args = [self.script_manager.script_dir_path + "\\" + self.script_manager.selected_item.text()]
        self.sp.start('python3', args)
        self.sp.readyRead.connect(self.dataReady)
        # self.robot_connection.connection_handler_single_com(fr"python2.7 {self.script_manager.script_dir_path}")
        # self.sp.setArguments(args)
        # self.sp.start()

    def stop_script(self):
        self.sp.kill()

    # def stop_script(self):
