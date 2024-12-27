from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QDialog
from model.java_engine import Java_Engine, compile_java
from model.chains import Assignment_Adjuster, Chat_Bot_Compile, Chat_Bot_Run
from view.dialogs import Dialog_Chapter, Dialog_Preferences, Dialog_Welcome

class Controller:
    """Learn Java's controller class."""

    def __init__(self, model, view):
        super(Controller,self).__init__()
        self._model = model
        self._view = view
        self._java_engine = None
        self._assignment_adjuster = None
        self._chat_bot = None
        self._communicator = Communicator()
        self._dialog_welcome = Dialog_Welcome()
        self._dialog_chapter = Dialog_Chapter(model=model)
        self._dialog_preferences = Dialog_Preferences(model=model)
        self._connectSignalsAndSlots()
        self._colors = ["white","lightgreen","lightcoral"]
        if self._model.new_user :
            self._show_welcome_page()
        else:
            self._model.set_starting_chapter()
            if self._model.get_preferences_set():
                self._adjust_assignments()
        self._set_code_file()
        self._set_tutorial()

    def _connectSignalsAndSlots(self):
        self._view.pB_compile.clicked.connect(self._compile_java_code)
        self._view.pB_run.clicked.connect(self._run_stop_java_program)
        self._view.lE_input.returnPressed.connect(self._send_input)
        self._view.lE_question.returnPressed.connect(self._send_question)
        self._communicator.java_program_stopped.connect(self._after_run)
        self._communicator.answer_sent.connect(self._answer_sent)
        self._view.action_Beenden.triggered.connect(self._exit_application)
        self._view.action_Kapitelwahl.triggered.connect(self._choose_chapter)
        self._view.action_increase_font_size.triggered.connect(self.increase_font_size)
        self._view.action_decrease_font_size.triggered.connect(self.decrease_font_size)
        self._view.action_zeige_Startinformationen.triggered.connect(self._dialog_welcome.exec)
        self._view.pB_next_Chapter.clicked.connect(self._next_chapter)
        self._view.pB_previous_Chapter.clicked.connect(self._previous_chapter)

    def _set_code_file(self):
        self._view.pTE_code.setPlainText(self._model.get_current_java_file())

    def _set_tutorial(self):
        html_content = self._model.get_tutorial_html(self._model.get_current_chapter(),self._view.get_font_size())
        self._view.tE_Tutorial.setHtml(html_content)

    def _update_output(self, output): #, colorNr=0):
        self._model.update_output(output) #,colorNr)

    def _send_input(self):
        self._model.set_input(self._view.lE_input.text())
        self._view.lE_input.clear()
        
    def _send_question(self):
        self._model.set_question(self._view.lE_question.text())
        self._view.lE_question.clear()
        
    def _answer_sent(self):
        self._view.tE_Informationen.setText(self._model.get_answer())
        self._view.tE_Informationen.setStyleSheet("")
        
    def _compile_java_code(self):
        if self._chat_bot is not None:
                self._chat_bot.stop()
        self._model.update_output("")  # clear output window
        self._model.set_current_java_file(self._view.pTE_code.toPlainText())
        self._view.pB_compile.setEnabled(False)
        self._view.lE_question.setEnabled(False)
        QApplication.processEvents()
        user_code = self._view.pTE_code.toPlainText()
        self._model.write_java_file(user_code)
        compile_result = compile_java()
        if (compile_result == "compilation successful"):
            color = 1
            self._view.pB_run.setEnabled(True)
            output = """Das kompilieren deines Codes hat geklappt.
Mit der Taste "start" kannst du dein Programm nun laufen lassen.""" 
        else:
            color = 2
            self._view.pB_run.setEnabled(False)
            self._view.lE_question.setEnabled(True)
            self._model.update_output(compile_result)
            QApplication.processEvents()
            output = self._model.compile_check(user_code=user_code,compile_result=compile_result)
            self._chat_bot = Chat_Bot_Compile(
                model=self._model,
                communicator=self._communicator,
                user_code=user_code,
                compile_result=compile_result,
                initial_response=output)
            self._chat_bot.start()
        self._view.tE_Informationen.setText(output)
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[color] + ";")
        self._view.pB_compile.setEnabled(True)
        
        

    def _run_stop_java_program(self):
        if self._view.pB_run.isChecked():
            if self._chat_bot is not None:
                self._chat_bot.stop()
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
        self._view.lE_question.setEnabled(True)
        self._set_start_button_text(False)
        user_code = self._view.pTE_code.toPlainText()
        output = self._model.get_output()
        assignment = self._model.get_assignment(self._model.get_current_chapter())
        topics = self._model.get_topics(self._model.get_current_chapter())
        input = self._view.lE_input.text()
        run_information = self._model.run_check(
            user_code=user_code,
            assignment=assignment,
            output=output,
            topics=topics,
            input=input)
        self._view.tE_Informationen.setText(run_information)
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[0] + ";")
        self._chat_bot = Chat_Bot_Run(
            model=self._model,
            communicator=self._communicator,
            user_code=user_code,
            assignment=assignment,
            topics=topics,
            input=input,
            output=output,
            initial_response=output)
        self._chat_bot.start()

    def _set_start_button_text(self, value):
        if value:
            self._view.pB_run.setText("stop")
        else:
            self._view.pB_run.setText("start")

    def increase_font_size(self):
        self._view.increase_font_size()
        self._set_tutorial()
    
    def decrease_font_size(self):
        self._view.decrease_font_size()
        self._set_tutorial()
    
    def _next_chapter(self):
        if (self._model.get_current_chapter() < self._model.get_max_chapter()):
            self._model.set_current_java_file(self._view.pTE_code.toPlainText())
            self._model.set_current_chapter(self._model.get_current_chapter() + 1)
            self._prepare_chapter()
            
    def _previous_chapter(self):
        if (self._model.get_current_chapter() > 1):
            self._model.set_current_java_file(self._view.pTE_code.toPlainText())
            self._model.set_current_chapter(self._model.get_current_chapter() - 1)
            self._prepare_chapter()
        

    def _choose_chapter(self):
        if (self._dialog_chapter.exec() == QDialog.DialogCode.Accepted): 
            self._model.set_current_chapter(int(self._dialog_chapter.cB_choose_chapter.currentText()))
            self._prepare_chapter()

    def _prepare_chapter(self):
        self._set_code_file()
        self._set_tutorial()
        self._view.pB_run.setEnabled(False)
        self._clear_information()
        self._model.clear_output()
        if self._chat_bot is not None:
                self._chat_bot.stop()
        self._view.lE_question.setEnabled(False)
                
    def _adjust_assignments(self):
        self._assignment_adjuster = Assignment_Adjuster(model=self._model)
        self._assignment_adjuster.start()             
    
    def _show_welcome_page(self):
        if (self._dialog_preferences.exec() == QDialog.DialogCode.Accepted):
            self._model.set_preferences(favorite_subjects=self._dialog_preferences.lE_Fach.text(),
                                    hobbies=self._dialog_preferences.lE_Hobbys.text(),
                                    profession=self._dialog_preferences.lE_Beruf.text(),
                                    other=self._dialog_preferences.pTE_Sonstiges.toPlainText())
            self._adjust_assignments()
        self._dialog_welcome.exec()
        self._prepare_chapter()    
            
            

    def _clear_information(self):
        self._view.tE_Informationen.clear()
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[0] + ";")

    def _exit_application(self):
        self._model.set_session_chapter()
        QApplication.instance().quit()


class Communicator(QObject):
    def __init__(self):
        super(Communicator,self).__init__()

    java_program_stopped = pyqtSignal()
    answer_sent = pyqtSignal()