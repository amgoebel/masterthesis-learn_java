from PyQt6.QtWidgets import QDialog
from view.UI_dialog_chapter import Ui_Dialog_Choose_Chapter
from view.UI_dialog_preferences import Ui_UI_Dialog_Preferences
from view.UI_dialog_welcome import Ui_UI_Dialog_Welcome


class Dialog_Chapter(QDialog, Ui_Dialog_Choose_Chapter):
    def __init__(self,model,parent=None):
        super(Dialog_Chapter, self).__init__()
        self.setupUi(self)
        self._model = model
        self._set_values()

    def _set_values(self):
        for i in range(1, self._model.get_max_chapter() + 1):
            self.cB_choose_chapter.addItem(str(i))

class Dialog_Preferences(QDialog, Ui_UI_Dialog_Preferences):
    def __init__(self,model,parent=None):
        super(Dialog_Preferences, self).__init__()
        self.setupUi(self)
        self._model = model

    def showEvent(self, event):
        self._set_values()
        # Call the base class implementation to ensure the event is handled properly
        super().showEvent(event)

    def _set_values(self):
        self.lE_Fach.setText(self._model.get_favorite_subjects())
        self.lE_Hobbys.setText(self._model.get_hobbies())
        self.lE_Beruf.setText(self._model.get_profession())
        


class Dialog_Welcome(QDialog, Ui_UI_Dialog_Welcome):
    def __init__(self,model,parent=None):
        super(Dialog_Welcome, self).__init__()
        self.setupUi(self)
        self._model = model

    def showEvent(self, event):
        self._set_values()
        # Call the base class implementation to ensure the event is handled properly
        super().showEvent(event)

    def _set_values(self):
        self.tE_Welcome.setText(self._model.get_welcome_html())