import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from view.view import MainWindow, Login_Dialog
from model.model import Model
from controller.controller import Controller
from controller.login_controller import Login_Controller


def main():
    """Learn Java's main function."""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("model/tutorial_files/e-learning-icon.png"))
    mymodel = Model()
    login_dialog = Login_Dialog()
    login_control = Login_Controller(model=mymodel,login_view=login_dialog)
    
    if login_dialog.exec():
        window = MainWindow(model=mymodel)
        window.show()
        control = Controller(model=mymodel,view=window)
        sys.exit(app.exec())

if (__name__ == "__main__"):
    main()