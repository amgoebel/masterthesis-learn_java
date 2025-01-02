from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QDialog
from model.java_engine import Java_Engine, compile_java
from model.chains import Assignment_Adjuster, Chat_Bot_Compile, Chat_Bot_Run
from view.dialogs import Dialog_Chapter, Dialog_Preferences, Dialog_Welcome

class Controller:
    # Controller class to manage interactions between the model and the view, handling user actions and updating the UI.

    def __init__(self, model, view):
        # Initialize the controller with the model and view, set up dialogs, and connect signals and slots.
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
        self._colors = ["white","lightgreen","lightcoral"]   # Colors for background of output window
        
        # Determine if the user is new and show the welcome page or 
        # set the starting chapter and continue adjusting the assignments if not already finished
        if self._model.new_user :
            self._show_welcome_page()
        else:
            self._model.set_starting_chapter()
            if self._model.get_preferences_set():
                self._adjust_assignments()
        
        # Set the initial code file and tutorial content
        self._set_code_file()
        self._set_tutorial()

    def _connectSignalsAndSlots(self):
        # Connect UI elements to their respective handler functions.
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
        # Set the current Java code in the code editor view.
        self._view.pTE_code.setPlainText(self._model.get_current_java_code())

    def _set_tutorial(self):
        # Set the tutorial content in the view based on the current chapter.
        html_content = self._model.get_tutorial_html(self._model.get_current_chapter(),self._view.get_font_size())
        self._view.tE_Tutorial.setHtml(html_content)

    def _update_output(self, output):
        # Update the output display in the view with the given output.
        self._model.update_output(output) 

    def _send_input(self):
        # Send user input from the input field to the model.
        self._model.set_input(self._view.lE_input.text())
        self._view.lE_input.clear()
        
    def _send_question(self):
        # Send user question from the question field to the model.
        self._model.set_question(self._view.lE_question.text())
        self._view.lE_question.clear()
        
    def _answer_sent(self):
        # Display the answer from the model in the information view.
        self._view.tE_Informationen.setText(self._model.get_answer())
        self._view.tE_Informationen.setStyleSheet("")
        
    def _compile_java_code(self):
        # Compile the Java code written by the user and handle the result.
        if self._chat_bot is not None:
                self._chat_bot.stop()    # stop running chat bot
        self._model.update_output("")  # clear output window
        user_code = self._view.pTE_code.toPlainText() # get java code
        self._model.set_current_java_code(user_code)  # update java code from view to model
        self._view.pB_compile.setEnabled(False)   # disable compile button
        self._view.lE_question.setEnabled(False)  # disable chat bot field
        QApplication.processEvents()              # update view
        self._model.write_java_file(user_code)    # write java code to file
        compile_result = compile_java()           # compile java code and get error message
        if (compile_result == "compilation successful"):
            color = 1                             # set background color to green
            self._view.pB_run.setEnabled(True)    # enable run button
            output = """Das kompilieren deines Codes hat geklappt.
Mit der Taste "start" kannst du dein Programm nun laufen lassen.""" 
        else:
            color = 2                             # set background color to red
            self._view.pB_run.setEnabled(False)   # disable run button
            self._model.update_output(compile_result)  # update model and view with error message from compiler
            output = self._model.compile_check(user_code=user_code,compile_result=compile_result) # get hint from LLM
            self._chat_bot = Chat_Bot_Compile(
                model=self._model,
                communicator=self._communicator,
                user_code=user_code,
                compile_result=compile_result,
                initial_response=output)
            self._chat_bot.start()                     # start chat bot
            self._view.lE_question.setEnabled(True)    # enable chat bot field
            QApplication.processEvents()               # update view
        self._view.tE_Informationen.setText(output)    # update the information window with the hint from the LLM
        self._view.tE_Informationen.setStyleSheet("background-color: " + self._colors[color] + ";")  # set background color
        self._view.pB_compile.setEnabled(True)         # enable compile button

    def _run_stop_java_program(self):
        # Start or stop the Java program based on the current state of the run button.
        if self._view.pB_run.isChecked():                    # start if there is no program running
            if self._chat_bot is not None:
                self._chat_bot.stop()                        # stop running chat bot
            self._view.lE_input.setEnabled(True)             # enable the input field for potential input
            QApplication.processEvents()                     # update view
            self._java_engine = Java_Engine(self._model, self._communicator)
            self._view.connect_java_engine(self._java_engine)
            self._java_engine.start()                        # run the java program
            self._set_start_button_text(True)                # set the text of the start/stop button to "stop"
        else:                                                # stop the running program
            self._java_engine.stop_signal.emit()
            self._set_start_button_text(False)               # set the text of the start/stop button to "start" 

    def _after_run(self):
        # Perform tasks after the Java program has run, such as updating the UI and starting the chat bot.
        self._view.pB_run.setChecked(False)                  # disable run button
        self._view.lE_input.setEnabled(False)                # disable the input field
        self._view.lE_question.setEnabled(True)              # disable the chat bot field 
        self._set_start_button_text(False)                   # set the text of the start/stop button to "start"             
        user_code = self._view.pTE_code.toPlainText()        # get the user_code
        output = self._model.get_output()                    # get the output of the program 
        assignment = self._model.get_assignment(self._model.get_current_chapter())  # get the current assignment
        topics = self._model.get_topics(self._model.get_current_chapter())  # get the current topics
        input = self._view.lE_input.text()                   # get the input sent during the run of the program
        run_information = self._model.run_check(             # get analysis form LLM of the run
            user_code=user_code,
            assignment=assignment,
            output=output,
            topics=topics,
            input=input)
        self._view.tE_Informationen.setText(run_information)  # update the information window with the hint from the LLM
        self._view.tE_Informationen.setStyleSheet("")         # reset the background color of the information window
        self._chat_bot = Chat_Bot_Run(
            model=self._model,
            communicator=self._communicator,
            user_code=user_code,
            assignment=assignment,
            topics=topics,
            input=input,
            output=output,
            initial_response=output)
        self._chat_bot.start()                                # start the chat bot

    def _set_start_button_text(self, value):
        # Set the text of the start/stop button based on the program's running state.
        if value:
            self._view.pB_run.setText("stop")
        else:
            self._view.pB_run.setText("start")

    def increase_font_size(self):
        # Increase the font size of the tutorial content.
        self._view.increase_font_size()
        self._set_tutorial()
    
    def decrease_font_size(self):
        # Decrease the font size of the tutorial content.
        self._view.decrease_font_size()
        self._set_tutorial()
    
    def _next_chapter(self):
        # Move to the next chapter in the tutorial.
        if (self._model.get_current_chapter() < self._model.get_max_chapter()):
            self._model.set_current_java_code(self._view.pTE_code.toPlainText())
            self._model.set_current_chapter(self._model.get_current_chapter() + 1)
            self._prepare_chapter()
            
    def _previous_chapter(self):
        # Move to the previous chapter in the tutorial.
        if (self._model.get_current_chapter() > 1):
            self._model.set_current_java_code(self._view.pTE_code.toPlainText())
            self._model.set_current_chapter(self._model.get_current_chapter() - 1)
            self._prepare_chapter()
        
    def _choose_chapter(self):
        # Open a dialog to choose a specific chapter.
        if (self._dialog_chapter.exec() == QDialog.DialogCode.Accepted): 
            self._model.set_current_chapter(int(self._dialog_chapter.cB_choose_chapter.currentText()))
            self._prepare_chapter()

    def _prepare_chapter(self):
        # Prepare the view and model for the selected chapter.
        self._set_code_file()                 # load the starting code for the current chapter
        self._set_tutorial()                  # load the tutorial content for the current chapter
        self._view.pB_run.setEnabled(False)   # enable the run button
        self._clear_information()             # clear the information window
        self._model.clear_output()            # clear the output for model and view
        if self._chat_bot is not None:
                self._chat_bot.stop()         # stop potential chat bot
        self._view.lE_question.setEnabled(False)   # disable chat bot field
                
    def _adjust_assignments(self):
        # Adjust assignments based on user preferences.
        self._assignment_adjuster = Assignment_Adjuster(model=self._model)
        self._assignment_adjuster.start()             
    
    def _show_welcome_page(self):
        # Show the welcome page and set user preferences if applicable.
        if (self._dialog_preferences.exec() == QDialog.DialogCode.Accepted):
            self._model.set_preferences(favorite_subjects=self._dialog_preferences.lE_Fach.text(),
                                    hobbies=self._dialog_preferences.lE_Hobbys.text(),
                                    profession=self._dialog_preferences.lE_Beruf.text(),
                                    other=self._dialog_preferences.pTE_Sonstiges.toPlainText())
            self._adjust_assignments()
        self._dialog_welcome.exec()
        self._prepare_chapter()          

    def _clear_information(self):
        # Clear the information display in the view.
        self._view.tE_Informationen.clear()
        self._view.tE_Informationen.setStyleSheet("")

    def _exit_application(self):
        # Exit the application and save the current session state.
        self._model.set_session_chapter()
        QApplication.instance().quit()


class Communicator(QObject):
    # Communicator class to communicate between the different threads of the model.

    def __init__(self):
        # Initialize the communicator class.
        super(Communicator, self).__init__()

    # Signal emitted when the Java program stops.
    java_program_stopped = pyqtSignal()
    # Signal emitted when an answer is sent.
    answer_sent = pyqtSignal()