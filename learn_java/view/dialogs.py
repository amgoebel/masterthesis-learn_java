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
        self._max_index = 11
        self._image_folder = os.path.dirname(__file__)
        self._text = ["Hier siehst du ein Bild vom Hauptfenster des Programms, das dir helfen soll Java zu lernen.\nDas Programm ist in verschiedene Bereiche aufgeteilt.",
                      "In diesem Bereich findest du zu jedem Kapitel eine Lektion und eine Aufgabe.\nLies dir die Lektion immer gut durch.",
                      "In diesem Bereich musst du deine Programmierung eingeben um die Aufgabe zu lösen.\n",
                      "In diesem Bereich erhältst du Informationen/Hilfe zu deiner Programmierung.\nEs kann manchmal ein paar Sekunden dauern bis die Hilfe angezeigt wird.",
                      "In dieser Zeile kannst du kurze Nachfragen zu der Hilfe stellen.\nWenn du \"Enter\" drückst, wird die Frage abgeschickt.",
                      "In diesem Bereich werden Fehlermeldungen und die Ausgaben\ndeiner Programmierung angezeigt.",
                      "In dieser Zeile kannst du Eingaben zu deinem Programm machen, wenn dies nötig ist.\nWenn du \"Enter\" drückst, wird die Eingabe an das Programm übergeben.",
                      "Mit diesen Tasten kannst du zum nächsten oder vorherigen Kapitel springen.\nDie Hilfe wird damit beendet.",
                      "Mit dieser Taste kannst du deine Programmierung kompilieren.\nDas bedeutet, dass deine Programmierung auf syntaktische Fehler überprüft wird.",
                      "Mit dieser Taste kannst du dein Programm starten. Falls es nicht von alleine\nstoppen sollte, kannst du es mit dieser Taste auch wieder anhalten.",
                      "Im Menü kannst du das Programm beenden, die Schriftgröße ändern und dir diese\nInformationen nochmal anzeigen lassen. Viel Spaß mit dem Programm!"
                      ]     
        self.load_image()
        
    def showEvent(self, event):
        # Call the base class implementation to ensure the event is handled properly
        super().showEvent(event)
    
    def load_image(self):
        """
        Load the current image into the QLabel.
        """
        if 0 <= self._current_index < self._max_index:
            pixmap = QPixmap(os.path.join(self._image_folder,f"Intro_{self._current_index}.png"))
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
            self._current_index = 0
            self.pB_next_page.setText("Nächste Seite")  # Change button text for the next run
            self.load_image()
            self.accept()
        
        
    
