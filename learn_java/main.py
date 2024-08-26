import sys
from PyQt6.QtWidgets import QApplication

from view.view import MainWindow
from model.model import Model
from controller.controller import Controller


def main():
    """Learn Java's main function."""
    app = QApplication(sys.argv)
    mymodel = Model()
    window = MainWindow(model=mymodel)
    window.show()
    control = Controller(model=mymodel,view=window)
    sys.exit(app.exec())

if (__name__ == "__main__"):
    main()