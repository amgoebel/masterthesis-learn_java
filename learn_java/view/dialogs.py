from PyQt6.QtWidgets import QDialog
from view.UI_dialog_chapter import Ui_Dialog_Choose_Chapter
from view.UI_dialog_preferences import Ui_UI_Dialog_Preferences
from view.UI_dialog_welcome import Ui_UI_Dialog_Welcome


class Dialog_Chapter(QDialog, Ui_Dialog_Choose_Chapter):
    def __init__(self,parent=None):
        super(Dialog_Chapter, self).__init__()
        self.setupUi(self)
        self._set_values()

    def _set_values(self):
        for i in range(1, 11):
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
        preferences = self._model.get_preferences()
        self.lE_Name.setText(preferences.get_name())
        self.lE_Alter.setText(preferences.get_age())
        self.lE_Fach.setText(preferences.get_subject())
        self.lE_Hobbys.setText(preferences.get_hobby())
        self.lE_Beruf.setText(preferences.get_profession())
        self.lE_Vorbild.setText(preferences.get_role_model())


class Dialog_Welcome(QDialog, Ui_UI_Dialog_Welcome):
    def __init__(self,parent=None):
        super(Dialog_Welcome, self).__init__()
        self.setupUi(self)

    def showEvent(self, event):
        self._set_values()
        # Call the base class implementation to ensure the event is handled properly
        super().showEvent(event)

    def _set_values(self):
        print("dummy2")