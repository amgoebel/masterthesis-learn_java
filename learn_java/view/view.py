from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication
from view.UI_MainWindow import Ui_MainWindow
from view.UI_dialog_login import Ui_UI_Dialog_Login


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # Main window class for the application, managing the main UI components.
    def __init__(self, model, *args, obj=None, **kwargs):
        # Initialize the main window with the model and set up UI components.
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = model
        self.lV_output.setModel(self.model)
        self.java_engine = None
        self.font = QApplication.font()
        self.font_size = 12
        self.font.setPointSize(self.font_size)
        QApplication.setFont(self.font)         

    def closeEvent(self,event):
        # Handle the close event to stop the Java engine if running.
        if (self.java_engine != None):
            self.java_engine.stop_signal.emit()
            self.java_engine.wait()

    def connect_java_engine(self,java_engine):
        # Connect the Java engine to the main window for execution control.
        self.java_engine = java_engine
        
    def get_font_size(self):
        # Get the current font size used in the application.
        return self.font_size
        
    def increase_font_size(self):
        # Increase the font size globally for the application.
        self.font_size += 1
        self.font.setPointSize(self.font_size)     # Set the font size
        QApplication.setFont(self.font)  # Apply the updated font globally
        
    def decrease_font_size(self):
        # Decrease the font size globally for the application.
        self.font_size -= 1
        self.font.setPointSize(self.font_size)     # Set the font size
        QApplication.setFont(self.font)  # Apply the updated font globally   

    
class Login_Dialog(QDialog,Ui_UI_Dialog_Login):
    # Dialog class for user login, handling user input and authentication.
    def __init__(self, *args, obj=None, **kwargs):
        # Initialize the login dialog and set up UI components.
        super(Login_Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)