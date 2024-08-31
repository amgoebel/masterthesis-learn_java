from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QDialog
from model.java_engine import Java_Engine
from view.dialogs import Dialog_Chapter, Dialog_Preferences, Dialog_Welcome

class Controller:
    """Learn Java's controller class."""

    def __init__(self, model, view):
        super(Controller,self).__init__()
        self._model = model
        self._view = view
        self._java_engine = None
        self._communicator = Communicator()
        self._dialog_welcome = Dialog_Welcome(model=model)
        self._dialog_chapter = Dialog_Chapter(model=model)
        self._dialog_preferences = Dialog_Preferences(model=model)
        self._connectSignalsAndSlots()
        self._set_code_file()
        self._set_tutorial()
        self._colors = ["white","lightgreen","lightcoral"]
        self._dialog_welcome.exec()

    def _connectSignalsAndSlots(self):
        self._view.pB_compile.clicked.connect(self._compile_java_code)
        self._view.pB_run.clicked.connect(self._run_stop_java_program)
        self._view.lE_input.returnPressed.connect(self._send_input)
        self._communicator.java_program_stopped.connect(self._after_run)
        self._view.action_Beenden.triggered.connect(self._exit_application)
        self._view.action_Kapitelwahl.triggered.connect(self._choose_chapter)
        self._view.action_Person.triggered.connect(self._edit_preferences)
        self._view.action_zeige_Startinformationen.triggered.connect(self._show_welcome_page)
        self._view.pB_next_Chapter.clicked.connect(self._next_chapter)

    def _set_code_file(self):
        self._view.pTE_code.setPlainText(self._model.get_current_java_file())

    def _set_tutorial(self):
        html_content = self._model.get_tutorial().get_tutorial_html(self._model.get_current_chapter())
        self._view.tE_Tutorial.setHtml(html_content)

    def _update_output(self, output): #, colorNr=0):
        self._model.update_output(output) #,colorNr)

    def _send_input(self):
        self._model.set_input(self._view.lE_input.text())
        self._view.lE_input.clear()
        
    def _compile_java_code(self):
        self._view.pB_compile.setEnabled(False)
        QApplication.processEvents()
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
        self._view.tE_Informationen.setText(compile_result)
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[color] + ";")
        self._view.pB_compile.setEnabled(True)

    def _run_stop_java_program(self):
        if self._view.pB_run.isChecked():
            self._view.lE_input.setEnabled(True)
            QApplication.processEvents()
            self._java_engine = Java_Engine(self._model, self._communicator)
            self._view.connect_java_engine(self._java_engine)
            self._java_engine.start()
            self._set_start_button_text(True)
        else:
            self._java_engine.stop_signal.emit()
            self._set_start_button_text(False)

    # perform tasks after run:
    def _after_run(self):
        self._view.pB_run.setChecked(False)
        self._view.lE_input.setEnabled(False)
        self._set_start_button_text(False)
        user_code = self._view.pTE_code.toPlainText()
        output = self._model.get_output()
        assignment = self._model.get_tutorial().get_assignment(self._model.get_current_chapter())
        topics = self._model.get_tutorial().get_topics(self._model.get_current_chapter())
        input = self._view.lE_input.text()
        run_information = self._model.run_check(user_code=user_code,assignment=assignment,output=output,topics=topics,input=input)
        self._view.tE_Informationen.setText(run_information)
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[0] + ";")

    def _set_start_button_text(self, value):
        if value:
            self._view.pB_run.setText("stop")
        else:
            self._view.pB_run.setText("start")

    def _next_chapter(self):
        if (self._model.get_current_chapter() < self._model.get_max_chapter()):
            self._model.set_current_chapter(self._model.get_current_chapter() + 1)
        self._set_code_file()
        self._set_tutorial()
        self._view.pB_run.setEnabled(False)
        self._clear_information()
        self._model.clear_output()

    def _choose_chapter(self):
        if (self._dialog_chapter.exec() == QDialog.DialogCode.Accepted): 
            self._model.set_current_chapter(int(self._dialog_chapter.cB_choose_chapter.currentText()))
            self._set_code_file()
            self._set_tutorial()
            self._view.pB_run.setEnabled(False)
            self._clear_information()
            self._model.clear_output()

    def _edit_preferences(self): 
        if (self._dialog_preferences.exec() == QDialog.DialogCode.Accepted):
            name = self._dialog_preferences.lE_Name.text()
            age = self._dialog_preferences.lE_Alter.text()
            subject = self._dialog_preferences.lE_Fach.text()
            hobby = self._dialog_preferences.lE_Hobbys.text()
            profession = self._dialog_preferences.lE_Beruf.text()
            role_model = self._dialog_preferences.lE_Vorbild.text()
            self._model.set_preferences(name,age,subject,hobby,profession,role_model)

    def _show_welcome_page(self):
        self._dialog_welcome.exec()

    def _clear_information(self):
        self._view.tE_Informationen.clear()
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[0] + ";")

    def _exit_application(self):
        QApplication.instance().quit()


class Communicator(QObject):
    def __init__(self):
        super(Communicator,self).__init__()

    java_program_stopped = pyqtSignal()