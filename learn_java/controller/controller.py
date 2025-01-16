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
        self.model = model
        self.view = view
        self.java_engine = None
        self.assignment_adjuster = None
        self.chat_bot = None
        self.communicator = Communicator()
        self.dialog_welcome = Dialog_Welcome()
        self.dialog_chapter = Dialog_Chapter(model=model)
        self.dialog_preferences = Dialog_Preferences(model=model)
        self.connectSignalsAndSlots()
        self.colors = ["white","lightgreen","lightcoral"]   # Colors for background of output window
        
        # Determine if the user is new and show the welcome page or 
        # set the starting chapter and continue adjusting the assignments if not already finished
        if self.model.new_user :
            self.show_welcome_page()
        else:
            self.model.set_starting_chapter()
            if self.model.get_preferences_set():
                self.adjust_assignments()
        
        # Set the initial code file and tutorial content
        self.set_code_file()
        self.set_tutorial()

    def connectSignalsAndSlots(self):
        # Connect UI elements to their respective handler functions.
        self.view.pB_compile.clicked.connect(self.compile_java_code)       # start compilation by button
        self.view.pB_run.clicked.connect(self.run_stop_java_program)       # start/stop program by button
        self.view.lE_input.returnPressed.connect(self.send_input)          # send input to program
        self.view.lE_question.returnPressed.connect(self.send_question)    # send question to chat bot
        self.communicator.java_program_stopped.connect(self.after_run)     # clean up after run by received signal
        self.communicator.answer_sent.connect(self.answer_sent)            # display answer from chat bot by received signal
        self.view.action_Beenden.triggered.connect(self.exit_application)  # close program by menu
        self.view.action_Kapitelwahl.triggered.connect(self.choose_chapter)  # choose chapter by menu
        self.view.action_increase_font_size.triggered.connect(self.increase_font_size)  # increase font size by menu
        self.view.action_decrease_font_size.triggered.connect(self.decrease_font_size)  # decrease font size by menu
        self.view.action_zeige_Startinformationen.triggered.connect(self.dialog_welcome.exec)  # show help by menu
        self.view.pB_next_Chapter.clicked.connect(self.next_chapter)       # choose next chapter by button
        self.view.pB_previous_Chapter.clicked.connect(self.previous_chapter)  # choose previous chapter by button
    
    ### Basic handling
    def set_code_file(self):
        # Set the current Java code in the code editor view.
        self.view.pTE_code.setPlainText(self.model.get_current_java_code())

    def set_tutorial(self):
        # Set the tutorial content in the view based on the current chapter.
        html_content = self.model.get_tutorial_html(self.model.get_current_chapter(),self.view.get_font_size())
        self.view.tE_Tutorial.setHtml(html_content)

    def update_output(self, output):
        # Update the output display in the view with the given output.
        self.model.update_output(output) 

    def send_input(self):
        # Send user input from the input field to the model.
        self.model.set_input(self.view.lE_input.text())
        self.view.lE_input.clear()
        
    def send_question(self):
        # Send user question from the question field to the model.
        self.model.set_question(self.view.lE_question.text())
        self.view.lE_question.clear()
        
    def answer_sent(self):
        # Display the answer from the model in the information view.
        self.view.tE_Informationen.setText(self.model.get_answer())
        self.view.tE_Informationen.setStyleSheet("")
    
    def set_start_button_text(self, value):
        # Set the text of the start/stop button based on the program's running state.
        if value:
            self.view.pB_run.setText("stop")
        else:
            self.view.pB_run.setText("start")

    def increase_font_size(self):
        # Increase the font size of the tutorial content.
        self.view.increase_font_size()
        self.set_tutorial()
    
    def decrease_font_size(self):
        # Decrease the font size of the tutorial content.
        self.view.decrease_font_size()
        self.set_tutorial()
    
    def clear_information(self):
        # Clear the information display in the view.
        self.view.tE_Informationen.clear()
        self.view.tE_Informationen.setStyleSheet("")
    
    def next_chapter(self):
        # Move to the next chapter in the tutorial.
        if (self.model.get_current_chapter() < self.model.get_max_chapter()):
            self.model.set_current_java_code(self.view.pTE_code.toPlainText())
            self.model.set_current_chapter(self.model.get_current_chapter() + 1)
            self.prepare_chapter()
            
    def previous_chapter(self):
        # Move to the previous chapter in the tutorial.
        if (self.model.get_current_chapter() > 1):
            self.model.set_current_java_code(self.view.pTE_code.toPlainText())
            self.model.set_current_chapter(self.model.get_current_chapter() - 1)
            self.prepare_chapter()
        
    def choose_chapter(self):
        # Open a dialog to choose a specific chapter.
        if (self.dialog_chapter.exec() == QDialog.DialogCode.Accepted): 
            self.model.set_current_chapter(int(self.dialog_chapter.cB_choose_chapter.currentText()))
            self.prepare_chapter()

    def prepare_chapter(self):
        # Prepare the view and model for the selected chapter.
        self.set_code_file()                 # load the starting code for the current chapter
        self.set_tutorial()                  # load the tutorial content for the current chapter
        self.view.pB_run.setEnabled(False)   # enable the run button
        self.clear_information()             # clear the information window
        self.model.clear_output()            # clear the output for model and view
        if self.chat_bot is not None:
                self.chat_bot.stop()         # stop potential chat bot
        self.view.lE_question.setEnabled(False)   # disable chat bot field
                
    def adjust_assignments(self):
        # Adjust assignments based on user preferences.
        self.assignment_adjuster = Assignment_Adjuster(model=self.model)
        self.assignment_adjuster.start()             
    
    def show_welcome_page(self):
        # Show the welcome page and set user preferences if applicable.
        if (self.dialog_preferences.exec() == QDialog.DialogCode.Accepted):
            self.model.set_preferences(favorite_subjects=self.dialog_preferences.lE_Fach.text(),
                                    hobbies=self.dialog_preferences.lE_Hobbys.text(),
                                    profession=self.dialog_preferences.lE_Beruf.text(),
                                    other=self.dialog_preferences.pTE_Sonstiges.toPlainText())
            self.adjust_assignments()
        self.dialog_welcome.exec()
        self.prepare_chapter()          
    
    ### Java handling   
    def compile_java_code(self):
        # Compile the Java code written by the user and handle the result.
        if self.chat_bot is not None:
                self.chat_bot.stop()    # stop running chat bot
        self.model.update_output("")  # clear output window
        user_code = self.view.pTE_code.toPlainText() # get java code
        self.model.set_current_java_code(user_code)  # update java code from view to model
        self.view.pB_compile.setEnabled(False)   # disable compile button
        self.view.lE_question.setEnabled(False)  # disable chat bot field
        QApplication.processEvents()              # update view
        self.model.write_java_file(user_code)    # write java code to file
        compile_result = compile_java()           # compile java code and get error message
        if (compile_result == "compilation successful"):
            color = 1                             # set background color to green
            self.view.pB_run.setEnabled(True)    # enable run button
            output = """Das kompilieren deines Codes hat geklappt.
Mit der Taste "start" kannst du dein Programm nun laufen lassen.""" 
        else:
            color = 2                             # set background color to red
            self.view.pB_run.setEnabled(False)   # disable run button
            self.model.update_output(compile_result)  # update model and view with error message from compiler
            QApplication.processEvents()              # update view
            output = self.model.compile_check(user_code=user_code,compile_result=compile_result) # get hint from LLM
            self.chat_bot = Chat_Bot_Compile(
                model=self.model,
                communicator=self.communicator,
                user_code=user_code,
                compile_result=compile_result,
                initial_response=output)
            self.chat_bot.start()                     # start chat bot
            self.view.lE_question.setEnabled(True)    # enable chat bot field
            QApplication.processEvents()               # update view
        self.view.tE_Informationen.setText(output)    # update the information window with the hint from the LLM
        self.view.tE_Informationen.setStyleSheet("background-color: " + self.colors[color] + ";")  # set background color
        self.view.pB_compile.setEnabled(True)         # enable compile button

    def run_stop_java_program(self):
        # Start or stop the Java program based on the current state of the run button.
        if self.view.pB_run.isChecked():                    # start if there is no program running
            if self.chat_bot is not None:
                self.chat_bot.stop()                        # stop running chat bot
            self.view.lE_input.setEnabled(True)             # enable the input field for potential input
            QApplication.processEvents()                     # update view
            self.java_engine = Java_Engine(self.model, self.communicator)
            self.view.connect_java_engine(self.java_engine)
            self.java_engine.start()                        # run the java program
            self.set_start_button_text(True)                # set the text of the start/stop button to "stop"
        else:                                                # stop the running program
            self.java_engine.stop_signal.emit()
            self.set_start_button_text(False)               # set the text of the start/stop button to "start" 

    def after_run(self):
        # Perform tasks after the Java program has run, such as updating the UI and starting the chat bot.
        self.view.pB_run.setChecked(False)                  # disable run button
        self.view.lE_input.setEnabled(False)                # disable the input field
        self.view.lE_question.setEnabled(True)              # disable the chat bot field 
        self.set_start_button_text(False)                   # set the text of the start/stop button to "start"             
        user_code = self.view.pTE_code.toPlainText()        # get the user_code
        output = self.model.get_output()                    # get the output of the program 
        assignment = self.model.get_assignment(self.model.get_current_chapter())  # get the current assignment
        topics = self.model.get_topics(self.model.get_current_chapter())  # get the current topics
        input = self.view.lE_input.text()                   # get the input sent during the run of the program
        run_information = self.model.run_check(             # get analysis form LLM of the run
            user_code=user_code,
            assignment=assignment,
            output=output,
            topics=topics,
            input=input)
        self.view.tE_Informationen.setText(run_information)  # update the information window with the hint from the LLM
        self.view.tE_Informationen.setStyleSheet("")         # reset the background color of the information window
        self.chat_bot = Chat_Bot_Run(
            model=self.model,
            communicator=self.communicator,
            user_code=user_code,
            assignment=assignment,
            topics=topics,
            input=input,
            output=output,
            initial_response=output)
        self.chat_bot.start()                                # start the chat bot

    def exit_application(self):
        # Exit the application and save the current session state.
        self.model.set_session_chapter()
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