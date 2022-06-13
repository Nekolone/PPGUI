from PySide6.QtWidgets import QTextEdit, QPushButton

from initial.utility import *


# QTextEdit.cursorForPosition().currentFrame()


class SlideDesigner:
    def __init__(self, window):
        self.window = window

        self._cur_pointer_pos = None

    """
    GETTERS & SETTERS
    """

    @property
    def cur_pointer_pos(self) -> int:
        return self._cur_pointer_pos

    @cur_pointer_pos.setter
    def cur_pointer_pos(self, value):
        self._cur_pointer_pos = value

    """
    TRIGGERS
    """

    # def set_file_path(self, label: QLabel):
    #     filepath = QFileDialog.getOpenFileUrl(caption="Select file")[0].toLocalFile()
    #     label.setText(filepath)

    def setup_triggers(self):
        slideOut = self.window.findChild(QTextEdit, "slideNoteOut")
        # slideOut.cursorPositionChanged.connect(lambda: self.get_new_pointer_pos(slideOut))

        self.window.findChild(QPushButton, "nextButton").clicked.connect(lambda: self.add_next(slideOut))
        self.window.findChild(QPushButton, "videoButton").clicked.connect(lambda: self.add_video(slideOut))
        self.window.findChild(QPushButton, "audioButton").clicked.connect(lambda: self.add_audio(slideOut))
        self.window.findChild(QPushButton, "pauseButton").clicked.connect(lambda: self.add_pause(slideOut))
        self.window.findChild(QPushButton, "setButton").clicked.connect(lambda: self.add_set(slideOut))
        self.window.findChild(QPushButton, "volumeButton").clicked.connect(lambda: self.add_volume(slideOut))
        self.window.findChild(QPushButton, "rmodeButton").clicked.connect(lambda: self.add_rmode(slideOut))
        self.window.findChild(QPushButton, "empButton").clicked.connect(lambda: self.add_emph(slideOut))
        self.window.findChild(QPushButton, "rspdButton").clicked.connect(lambda: self.add_rspd(slideOut))
        self.window.findChild(QPushButton, "surveyButton").clicked.connect(lambda: self.add_survey(slideOut))
        self.window.findChild(QPushButton, "doButton").clicked.connect(lambda: self.add_do(slideOut))
        self.window.findChild(QPushButton, "resetButton").clicked.connect(lambda: self.add_reset(slideOut))
        # self.window.findChild(QPushButton, "delScriptButton").clicked.connect(
        #     lambda: self.delete_cur_script())
        # slideOut.textChanged.connect(lambda: self.get_new_pointer_pos(slideOut))
        # slideOut.clicked.connect(lambda: self.get_new_pointer_pos(slideOut))

    def add_next(self, item: QTextEdit):
        item.textCursor().insertText("<next/>")

    def add_video(self, item: QTextEdit):
        item.textCursor().insertText("<video> </video>")

    def add_audio(self, item: QTextEdit):
        item.textCursor().insertText("<audio> </audio>")

    def add_pause(self, item: QTextEdit):
        outline: QLineEdit = self.window.findChild(QLineEdit, "pauseLine")
        time = outline.text()
        if not time:
            item.textCursor().insertText(f"<pause time=\"100\"/>")
            return
        item.textCursor().insertText(f"<pause time=\"{time}\"/>")

    def add_set(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "setLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<set voice=\"neutral\"/>")
            return
        item.textCursor().insertText(f"<set voice=\"{data}\"/>")

    def add_volume(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "volumeLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<vol value=\"100\"> </vol>")
            return
        item.textCursor().insertText(f"<vol value=\"{data}\"> </vol>")

    def add_rmode(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "rmodeLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<rmode mode=\"sent\"> </rmode>")
            return
        item.textCursor().insertText(f"<rmode mode=\"{data}\"> </rmode>")

    def add_emph(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "empLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<emph word=\"    \" pos=\"1\"/>")
            return
        item.textCursor().insertText(f"<emph word=\"{data}\" pos=\"1\"/>")

    def add_rspd(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "rspdLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<rspd speed=\"100\"> </rspd>")
            return
        item.textCursor().insertText(f"<rspd speed=\"{data}\"> </rspd>")

    def add_survey(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "surveyLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"""
<startsurvey id=\"1\"> 
    <survey id="1">
        <pin>0A2X</pin>
        <type>auto</type>
        <questions>
            <question>
                <q>Question?</q>
                <timelimit>10</timelimit>
                <validoption>1</validoption>
                <options>
                    <o>Answer 1</o>
                    <o>Answer 2</o>
                    <o>Answer 3</o>
                </options>
            </question>
        </questions>
    </survey> 
</startsurvey>""")
            return
        item.textCursor().insertText(f"""
<startsurvey id="{data}"> 
    <survey id="{data}">
        <pin>0A2X</pin>
        <type>auto</type>
        <questions>
            <question>
                <q>Question?</q>
                <timelimit>10</timelimit>
                <validoption>1</validoption>
                <options>
                    <o>Answer 1</o>
                    <o>Answer 2</o>
                    <o>Answer 3</o>
                </options>
            </question>
        </questions>
    </survey> 
</startsurvey>""")

    def add_do(self, item: QTextEdit):
        outline = self.window.findChild(QLineEdit, "doLine")
        data = outline.text()
        if not data:
            item.textCursor().insertText(f"<do animation=\"{data}\"> </do>")
            return
        item.textCursor().insertText(f"<do animation=\"{data}\"> </do>")

    def add_reset(self, item: QTextEdit):
        item.textCursor().insertText("<rst/>")

    # def get_new_pointer_pos(self, item: QTextEdit):
    #     cur_pointer_pos = item.textCursor().position()
    # print(item.textCursor().position())

    """
    DESIGN
    """

    def make_shiny(self):
        pass
        # self.setup_table()
        # while self.inf_status:
        #     time.sleep(1)

        # QTextEdit.cursorForPosition().currentFrame()

    # def setup_table(self):
    #     self.update_script_table()
    # QListWidget.addItem(self.window.findChild(QPushButton, "pptxAddButton"))
    # self.window.findChild(QListWidget, "pptxAvailableTable").addItem("123")
    # self.window.findChild(QTableWidget, "pptxAvailableTable").setColumnWidth(1, 118)
    # self.window.findChild(QTableWidget, "pptxAvailableTable").setItem(1,1,QTableWidgetItem("зызызыз"))
