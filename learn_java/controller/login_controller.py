class Login_Controller:
    # Controller class to manage the login dialog, handling user authentication and registration.

    def __init__(self, model, login_view):
        # Initialize the login controller with the model and login view, and set up signal connections.
        super(Login_Controller, self).__init__()
        self.model = model
        self.login_view = login_view 
        self.connectSignalsAndSlots()  # Set up connections between UI elements and handler functions.
        self.register = False          # Flag for new user 
        # Initially hide the confirm password fields.
        self.login_view.l_confirm_password.setVisible(False)
        self.login_view.lE_confirm_password.setVisible(False)
        # Set default button behavior based on which input field is focused.
        self.login_view.lE_username.focusInEvent = lambda event: self.set_default_button(self.login_view.pB_login)
        self.login_view.lE_password.focusInEvent = lambda event: self.set_default_button(self.login_view.pB_login)
        self.login_view.lE_confirm_password.focusInEvent = lambda event: self.set_default_button(self.login_view.pB_new_user)

    def connectSignalsAndSlots(self):
        # Connect login and registration buttons to their respective handler functions.
        self.login_view.pB_new_user.clicked.connect(self.new_user)
        self.login_view.pB_login.clicked.connect(self.login)

    def set_default_button(self, button):
        # Set the default button for the login dialog based on the focused input field.
        self.login_view.pB_login.setDefault(False)  # Reset default state for login button.
        self.login_view.pB_new_user.setDefault(False)  # Reset default state for new user button.
        button.setDefault(True)  # Set the specified button as the default.

    def new_user(self):
        # Handle the creation of a new user, including password confirmation and user data setup.
        if not self.register:
            # If register button is pressed for the first time, show confirm password fields.
            self.register = True
            self.login_view.l_confirm_password.setVisible(True)
            self.login_view.lE_confirm_password.setVisible(True)
            self.login_view.pB_new_user.setText("Neuen Nutzer anlegen")  # Change button text.
            self.login_view.l_status_info.setText("Bestätige bitte dein Passwort")  # Update status info.
            self.login_view.lE_confirm_password.setFocus()  # Focus on confirm password field.

        else:
            # If register button is pressed again, attempt to create a new user.
            username = self.login_view.lE_username.text()
            password = self.login_view.lE_password.text()
            password_confirm = self.login_view.lE_confirm_password.text()
            if password == password_confirm:
                # Check if passwords match.
                if self.model.add_user(username, password):
                    # Attempt to add user to the model.
                    self.login_view.accept()  # Close dialog on success.
                else:
                    self.login_view.l_status_info.setText("Benutzer existiert bereits")  # User already exists.
            else:
                # If passwords do not match, clear fields and show error message.
                self.login_view.lE_username.clear()
                self.login_view.lE_password.clear()
                self.login_view.lE_confirm_password.clear()
                self.login_view.lE_username.setFocus()
                self.login_view.l_status_info.setText("Passwörter sind nicht gleich")  # Passwords do not match.

    def login(self):
        # Authenticate the user and close the dialog on successful login.
        username = self.login_view.lE_username.text()
        password = self.login_view.lE_password.text()
        if self.model.authenticate_user(username, password):
            # Check if user credentials are valid.
            self.login_view.accept()  # Close dialog on success.
        else:
            # If authentication fails, clear fields and show error message.
            self.login_view.lE_username.clear()
            self.login_view.lE_password.clear()
            self.login_view.lE_confirm_password.clear()
            self.login_view.lE_username.setFocus()
            self.login_view.l_status_info.setText("Benutzername oder Passwort falsch")  # Incorrect username or password.