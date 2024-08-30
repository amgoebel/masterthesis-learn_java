import os
import subprocess
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex
from PyQt6.QtGui import QBrush, QColor

class Handling(QAbstractListModel):
    def __init__(self):
        super(Handling,self).__init__()
        self.file_path = os.path.dirname(__file__)
        self.java_output = ""
        self.java_input = ""
        self._current_file = 1
        self._output = ""
        self._input = ""
        self._input_sent = False
        self._preferences = Preferences()
        #self._color = QColor("white")

    # methods for data handling:
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._output)
        #elif role == Qt.ItemDataRole.BackgroundRole:
        #    return QBrush(self._color)
        return None
    
    def setData(self, index, output, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._output = output
            self.dataChanged.emit(index, index)
            return True
        return False

    def update_output(self, output): #, colorNr=0):
        self.setData(self.index(0), output)
        #self.setBackgroundColor(colorNr=colorNr)

    def get_output(self):
        return(self.data(self.index(0)))
    
    def clear_output(self):
        self.update_output("")   
    
    # not used in the moment:
    def setBackgroundColor(self, colorNr=0):
        colors = ["white","lightgreen","lightcoral"]
        self._color = QColor(colors[colorNr])
        self.dataChanged.emit(self.index(0), self.index(0), [Qt.ItemDataRole.BackgroundRole])

    def rowCount(self, index=QModelIndex()):
        return 1  # We only have one item
    
    # receive input
    def set_input(self,input):
        self._input = input
        self.set_input_sent(True)

    def set_input_sent(self,value):
        self._input_sent = value

    def get_input(self):
        return self._input    
    
    def get_input_sent(self):
        return self._input_sent

    # change working directory
    def set_working_directory(self):
        try:
            os.chdir(self.file_path + "/java_files")
        except:
            print("... there was an error setting the working directory")

    # get current start file
    def get_current_java_file(self):
        self.set_working_directory()
        filename = "java" + str(self._current_file) + ".txt"
        f = open(filename,"r")
        code = f.read()
        f.close()
        return(code)
    
    # set current chapter
    def set_current_chapter(self,chapter):
        self._current_file = chapter

        # set current chapter
    def get_current_chapter(self):
        return self._current_file
    
    def set_preferences(self,name,age,subject,hobby,profession,role_model):
        self._preferences.set_preferences(name=name,age=age,subject=subject,hobby=hobby,profession=profession,role_model=role_model)
    
    def get_preferences(self):
        return self._preferences    
    
    # write to file
    def write_java_file(self, user_code):
        self.set_working_directory()
        print("writing java code to file ...")
        try:
            f = open("main.java","w")
            f.write(user_code)
            f.close()
            print("... code successfully written to file")
        except:
            print("... there was an error writing to file")


    # compile java code
    def compile_java(self):
        self.set_working_directory()
        print("starting compilation ...")
        try:
            p = subprocess.run(["javac","main.java"], capture_output=True, text=True, check=True)
            print("... compilation successful")
            error_code = "compilation successful"
        except subprocess.CalledProcessError as e: 
            print("... compilation failed")
            print("Error message: ", e.stderr)
            error_code = "Error message: " + e.stderr
        return(error_code)
    
class Preferences:
    def __init__(self):
        super(Preferences,self).__init__()
        self._name = ""
        self._age = ""
        self._subject = ""
        self._hobby = ""
        self._profession = ""
        self._role_model = ""
    
    def set_preferences(self,name,age,subject,hobby,profession,role_model):
        self._name = name
        self._age = age
        self._subject = subject
        self._hobby = hobby
        self._profession = profession
        self._role_model = role_model

    def get_name(self):
        return self._name
    
    def get_age(self):
        return self._age
    
    def get_subject(self):
        return self._subject

    def get_hobby(self):
        return self._hobby
    
    def get_profession(self):
        return self._profession
    
    def get_role_model(self):
        return self._role_model