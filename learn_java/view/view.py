from PyQt6 import QtWidgets
from view.UI_MainWindow import Ui_MainWindow


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

    