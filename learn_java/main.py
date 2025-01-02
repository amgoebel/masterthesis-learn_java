import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from view.view import MainWindow, Login_Dialog
from model.model import Model
from controller.controller import Controller
from controller.login_controller import Login_Controller

def main():
    # Main function to initialize the application, set up the model, and start the main window after login.
    
    # Create an instance of the QApplication
    app = QApplication(sys.argv)
    
    # Determine the file path based on whether the script is frozen (e.g., packaged with PyInstaller) or not
    if getattr(sys, 'frozen', False):
        file_path = os.path.dirname(sys.executable)
    elif __file__:
        file_path = os.path.dirname(__file__)
    
    # Attempt to change the current working directory to the determined file path
    try:
        os.chdir(file_path)
    except:
        print("... there was an error setting the working directory")
    
    # Set the application window icon
    app.setWindowIcon(QIcon("e-learning-icon.png"))
    
    # Initialize the model
    mymodel = Model()
    
    # Initialize the login dialog and its controller
    login_dialog = Login_Dialog()
    login_control = Login_Controller(model=mymodel, login_view=login_dialog)

    # Execute the login dialog and if successful, show the main window
    if login_dialog.exec():
        window = MainWindow(model=mymodel)
        window.show()
        
        # Initialize the main controller
        control = Controller(model=mymodel, view=window)
        
        # Start the application event loop
        sys.exit(app.exec())

# Entry point of the application
if __name__ == "__main__":
    main()