import os
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
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
        self.pTE_Sonstiges.setPlainText(self._model.get_other())
        


class Dialog_Welcome(QDialog, Ui_UI_Dialog_Welcome):
    def __init__(self,parent=None):
        super(Dialog_Welcome, self).__init__()
        self.setupUi(self)
        self.pB_next_page.clicked.connect(self.next_image)
        self._current_index = 0
        self._max_index = 10
        self._image_folder = os.path.dirname(__file__)
        self._text = ["hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo",
                      "hallo"]     
        self.load_image()
        
    def showEvent(self, event):
        # Call the base class implementation to ensure the event is handled properly
        super().showEvent(event)
    
    def load_image(self):
        """
        Load the current image into the QLabel.
        """
        if 0 <= self._current_index < self._max_index:
            pixmap = QPixmap(os.path.join(self._image_folder,f"Intro_{self._current_index+1}.png"))
            self.l_image.setPixmap(pixmap)
            self.l_text.setText(self._text[self._current_index])

    def next_image(self):
        """
        Move to the next image or terminate the program if the last image is reached.
        """
        self._current_index += 1
        if self._current_index < self._max_index:
            self.load_image()
            if self._current_index == self._max_index - 1:
                self.pB_next_page.setText("OK")  # Change button text on the last image
        else:
            self.accept()
        
        
    
