class Login_Controller:
    # Controller class to manage the login dialog, handling user authentication and registration.

    def __init__(self, model, login_view):
        # Initialize the login controller with the model and login view, and set up signal connections.
        super(Login_Controller, self).__init__()
        self._model = model
        self._login_view = login_view 
        self._connectSignalsAndSlots()  # Set up connections between UI elements and handler functions.
        self._register = False          # Flag for new user 
        # Initially hide the confirm password fields.
        self._login_view.l_confirm_password.setVisible(False)
        self._login_view.lE_confirm_password.setVisible(False)
        # Set default button behavior based on which input field is focused.
        self._login_view.lE_username.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_login)
        self._login_view.lE_password.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_login)
        self._login_view.lE_confirm_password.focusInEvent = lambda event: self._set_default_button(self._login_view.pB_new_user)

    def _connectSignalsAndSlots(self):
        # Connect login and registration buttons to their respective handler functions.
        self._login_view.pB_new_user.clicked.connect(self._new_user)
        self._login_view.pB_login.clicked.connect(self._login)

    def _set_default_button(self, button):
        # Set the default button for the login dialog based on the focused input field.
        self._login_view.pB_login.setDefault(False)  # Reset default state for login button.
        self._login_view.pB_new_user.setDefault(False)  # Reset default state for new user button.
        button.setDefault(True)  # Set the specified button as the default.

    def _new_user(self):
        # Handle the creation of a new user, including password confirmation and user data setup.
        if not self._register:
            # If register button is pressed for the first time, show confirm password fields.
            self._register = True
            self._login_view.l_confirm_password.setVisible(True)
            self._login_view.lE_confirm_password.setVisible(True)
            self._login_view.pB_new_user.setText("Neuen Nutzer anlegen")  # Change button text.
            self._login_view.l_status_info.setText("Bestätige bitte dein Passwort")  # Update status info.
            self._login_view.lE_confirm_password.setFocus()  # Focus on confirm password field.

        else:
            # If register button is pressed again, attempt to create a new user.
            username = self._login_view.lE_username.text()
            password = self._login_view.lE_password.text()
            password_confirm = self._login_view.lE_confirm_password.text()
            if password == password_confirm:
                # Check if passwords match.
                if self._model.add_user(username, password):
                    # Attempt to add user to the model.
                    self._login_view.accept()  # Close dialog on success.
                else:
                    self._login_view.l_status_info.setText("Benutzer existiert bereits")  # User already exists.
            else:
                # If passwords do not match, clear fields and show error message.
                self._login_view.lE_username.clear()
                self._login_view.lE_password.clear()
                self._login_view.lE_confirm_password.clear()
                self._login_view.lE_username.setFocus()
                self._login_view.l_status_info.setText("Passwörter sind nicht gleich")  # Passwords do not match.

    def _login(self):
        # Authenticate the user and close the dialog on successful login.
        username = self._login_view.lE_username.text()
        password = self._login_view.lE_password.text()
        if self._model.authenticate_user(username, password):
            # Check if user credentials are valid.
            self._login_view.accept()  # Close dialog on success.
        else:
            # If authentication fails, clear fields and show error message.
            self._login_view.lE_username.clear()
            self._login_view.lE_password.clear()
            self._login_view.lE_confirm_password.clear()
            self._login_view.lE_username.setFocus()
            self._login_view.l_status_info.setText("Benutzername oder Passwort falsch")  # Incorrect username or password.