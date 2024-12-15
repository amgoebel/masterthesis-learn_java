from view.dialogs import Dialog_Preferences, Dialog_Welcome


class Login_Controller:
    """Learn Java's controller class."""

    def __init__(self, model, login_view):
        super(Login_Controller,self).__init__()
        self._model = model
        self._login_view = login_view
        self._connectSignalsAndSlots()
        self._register = False # has the register button been pushed already? 
        self._login_view.l_confirm_password.setVisible(False)
        self._login_view.lE_confirm_password.setVisible(False)
        self._login_view.lE_username.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_login)
        self._login_view.lE_password.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_login)
        self._login_view.lE_confirm_password.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_new_user)
        

    def _connectSignalsAndSlots(self):
        self._login_view.pB_new_user.clicked.connect(self._new_user)
        self._login_view.pB_login.clicked.connect(self._login)
        
    def _set_default_button(self, button):
        self._login_view.pB_login.setDefault(False)
        self._login_view.pB_new_user.setDefault(False)
        button.setDefault(True)
        
    def _new_user(self):
        if not self._register :
            self._register = True
            self._login_view.l_confirm_password.setVisible(True)
            self._login_view.lE_confirm_password.setVisible(True)
            self._login_view.pB_new_user.setText("Neuen Nutzer anlegen")
            self._login_view.l_status_info.setText("Bestätige bitte dein Passwort")
            self._login_view.lE_confirm_password.setFocus()
        
        else:
            username = self._login_view.lE_username.text()
            password = self._login_view.lE_password.text()
            password_confirm = self._login_view.lE_confirm_password.text()
            if password == password_confirm :
                if self._model.add_user(username, password):
                    self._login_view.accept()  # Close dialog on success
                else :
                    self._login_view.l_status_info.setText("Benutzer existiert bereits")
            else:
                self._login_view.lE_username.clear()
                self._login_view.lE_password.clear()
                self._login_view.lE_confirm_password.clear()
                self._login_view.lE_username.setFocus()
                self._login_view.l_status_info.setText("Passwörter sind nicht gleich")
                
    def _login(self):
        username = self._login_view.lE_username.text()
        password = self._login_view.lE_password.text()
        if self._model.authenticate_user(username, password):
            self._login_view.accept()  # Close dialog on success
        else:
            self._login_view.lE_username.clear()
            self._login_view.lE_password.clear()
            self._login_view.lE_confirm_password.clear()
            self._login_view.lE_username.setFocus()
            self._login_view.l_status_info.setText("Benutzername oder Passwort falsch")