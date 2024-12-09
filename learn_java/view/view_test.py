from PyQt6.QtWidgets import QDialog
from view.UI_dialog_login import Ui_UI_Dialog_Login


class Login_Dialog(QDialog,Ui_UI_Dialog_Login):
    def __init__(self, *args, obj=None, **kwargs):
        super(Login_Dialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

    