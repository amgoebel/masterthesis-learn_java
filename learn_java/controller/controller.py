from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QDialog
from model.java_engine import Java_Engine
from view.dialogs import Dialog_Chapter

class Controller:
    """Learn Java's controller class."""

    def __init__(self, model, view):
        super(Controller,self).__init__()
        self._model = model
        self._view = view
        self._java_engine = None
        self._communicator = Communicator()
        self._dialog = Dialog_Chapter()
        self._connectSignalsAndSlots()
        self._set_code_file()

    def _connectSignalsAndSlots(self):
        self._view.pB_compile.clicked.connect(self._compile_java_code)
        self._view.pB_run.clicked.connect(self._run_stop_java_program)
        self._view.lE_input.returnPressed.connect(self._send_input)
        self._communicator.java_program_stopped.connect(self._disable_stop_button)
        self._view.action_Beenden.triggered.connect(self._exit_application)
        self._view.action_Kapitelwahl.triggered.connect(self._choose_chapter)
        self._view.pB_next_Chapter.clicked.connect(self._next_chapter)

    def _set_code_file(self):
        self._view.pTE_code.setPlainText(self._model.get_current_java_file())

    def _update_output(self, output): #, colorNr=0):
        self._model.update_output(output) #,colorNr)

    def _send_input(self):
        self._model.set_input(self._view.lE_input.text())
        self._view.lE_input.clear()
        
    def _compile_java_code(self):
        user_code = self._view.pTE_code.toPlainText()
        self._model.write_java_file(user_code)
        compile_result = self._model.compile_java()
        if (compile_result == "compilation successful"):
            color = 1
            self._view.pB_run.setEnabled(True)
            compile_result = """Das kompilieren deines Codes hat geklappt.
Mit der Taste "start" kannst du dein Programm nun laufen lassen.""" 
        else:
            color = 2
            self._view.pB_run.setEnabled(False)
            compile_result = self._model.compile_check(user_code=user_code,compile_result=compile_result)    
        self._view.tB_Informationen.setText(compile_result)
        colors = ["white","lightgreen","lightcoral"]
        self._view.tB_Informationen.setStyleSheet("background-color: " + colors[color] + ";")

    def _run_stop_java_program(self):
        if self._view.pB_run.isChecked():
            self._java_engine = Java_Engine(self._model, self._communicator)
            self._java_engine.start()
            self._set_start_button_text(True)
        else:
            self._java_engine.stop()
            self._set_start_button_text(False)

    def _disable_stop_button(self):
        self._view.pB_run.setChecked(False)
        self._set_start_button_text(False)

    def _set_start_button_text(self, value):
        if value:
            self._view.pB_run.setText("stop")
        else:
            self._view.pB_run.setText("start")

    def _next_chapter(self):
        self._model.set_current_chapter(self._model.get_current_chapter() + 1)
        self._set_code_file()

    def _choose_chapter(self):
        if (self._dialog.exec() == QDialog.DialogCode.Accepted): 
            self._model.set_current_chapter(int(self._dialog.cB_choose_chapter.currentText()))
            self._set_code_file()
        else:
            print("not dummy")

    def _exit_application(self):
        QApplication.instance().quit()


class Communicator(QObject):
    def __init__(self):
        super(Communicator,self).__init__()

    java_program_stopped = pyqtSignal()