from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog
from view.UI_MainWindow import Ui_MainWindow
from view.UI_dialog_login import Ui_UI_Dialog_Login


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, model, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self._model = model
        self.lV_output.setModel(self._model)
        self._java_engine = None

    def closeEvent(self,event):
        if (self._java_engine != None):
            self._java_engine.stop_signal.emit()
            self._java_engine.wait()

    def connect_java_engine(self,java_engine):
        self._java_engine = java_engine

    
class Login_Dialog(QDialog,Ui_UI_Dialog_Login):
    def __init__(self, *args, obj=None, **kwargs):
        super(Login_Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)