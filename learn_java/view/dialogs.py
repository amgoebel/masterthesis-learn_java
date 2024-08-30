from PyQt6.QtWidgets import QDialog
from view.UI_dialog_chapter import Ui_Dialog_Choose_Chapter
from view.UI_dialog_preferences import Ui_UI_Dialog_Preferences


class Dialog_Chapter(QDialog, Ui_Dialog_Choose_Chapter):
    def __init__(self,parent=None):
        super(Dialog_Chapter, self).__init__()
        self.setupUi(self)
        self._set_values()

    def _set_values(self):
        for i in range(1, 11):
            self.cB_choose_chapter.addItem(str(i))

class Dialog_Preferences(QDialog, Ui_UI_Dialog_Preferences):
    def __init__(self,parent=None):
        super(Dialog_Preferences, self).__init__()
        self.setupUi(self)