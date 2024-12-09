import os
import json
import bcrypt
from pathlib import Path
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QCoreApplication
from PyQt6.QtGui import QColor

class Handling(QAbstractListModel):
    # handles all 
    def __init__(self):
        super(Handling,self).__init__()
        self.json_user_path = Path("users.json")
        self.json_tutorial_path = Path("tutorial.json")
        self.file_path = os.path.dirname(__file__)
        self.username = ""
        self.new_user = False
        self.java_output = ""
        self.java_input = ""
        self._current_chapter = 1
        self._max_chapter = 25
        self._output = ""
        self._input = ""
        self._input_sent = False 

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
            QCoreApplication.processEvents()
            return True
        return False

    def update_output(self, output): 
        self.setData(self.index(0), output)

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
    def set_working_directory_java(self):
        try:
            os.chdir(self.file_path + "/java_files")
        except:
            print("... there was an error setting the working directory")
            
    def set_working_directory_tutorial(self):
        try:
            os.chdir(self.file_path + "/tutorial_files")
        except:
            print("... there was an error setting the working directory")

    # get current start file
    def get_current_java_file(self):
        data = self.load_user_data(self.username)        
        text = data[self._current_chapter - 1]['java']
        return text
    
    def set_current_java_file(self,code):
        data = self.load_user_data(self.username)   
        data[self._current_chapter - 1]['java'] = code
        self.save_user_data(self.username,data)
        
    def get_java_file(self,chapter_nr):
        data = self.load_user_data(self.username)
        text = data[chapter_nr - 1]['java']
        return text
    
    def get_original_java_file(self,chapter_nr):
        data = self.load_tutorial_data()
        text = data['tutorial'][chapter_nr - 1]['java']
        return text
    
    def set_java_file(self,chapter_nr,code):
        data = self.load_user_data(self.username)        
        data[chapter_nr - 1]['java'] = code
        self.save_user_data(self.username,data)
        
    def get_tutorial_html(self,chapter_nr):
        data = self.load_tutorial_data()
        data2 = self.load_user_data(self.username)
        text = data['html_head']
        text += data['tutorial'][chapter_nr - 1]['content']
        text += data2[chapter_nr - 1]['assignment']
        text += data['html_tail']
        return text
    
    def get_assignment(self,chapter_nr):
        data = self.load_user_data(self.username) 
        text = data[chapter_nr - 1]['assignment']
        return text  
    
    def set_assignment(self,chapter_nr,assignment):
        data = self.load_user_data(self.username)        
        data[chapter_nr - 1]['assignment'] = assignment
        self.save_user_data(self.username,data)
        
    def get_original_assignment(self,chapter_nr):
        data = self.load_tutorial_data()        
        text = data['tutorial'][chapter_nr - 1]['assignment']
        return text
    
    def get_topics(self,chapter_nr):
        data = self.load_tutorial_data()        
        text = "topics:"+"\n"
        for chapter in range(chapter_nr):
            text += data['tutorial'][chapter]['topic'] + "\n"
        return text
    
    # set current chapter
    def set_current_chapter(self,chapter):
        self._current_chapter = chapter
        
    # set chapter from last session
    def set_starting_chapter(self):
        data = self.load_data()
        self._current_chapter = data[self.username]['current_chapter']
        
    # set user preferences
    def set_preferences(self, favorite_subjects, hobbies,profession, other):
        data = self.load_data()
        data[self.username]['preferences']['favorite_subjects'] = favorite_subjects
        data[self.username]['preferences']['hobbies'] = hobbies
        data[self.username]['preferences']['profession'] = profession
        data[self.username]['preferences']['other'] = other
        self.save_data(data)
        
    # get from preferences
    def get_favorite_subjects(self):
        data = self.load_data()
        return data[self.username]['preferences']['favorite_subjects']
    
    def get_hobbies(self):
        data = self.load_data()
        return data[self.username]['preferences']['hobbies']
    
    def get_profession(self):
        data = self.load_data()
        return data[self.username]['preferences']['profession']
    
    def get_other(self):
        data = self.load_data()
        return data[self.username]['preferences']['other']
  
    # set chapter for next last session
    def set_session_chapter(self):
        data = self.load_data()
        data2 = data.get(self.username, {})
        data2["current_chapter"] = self._current_chapter
        self.save_data(data)
        
    # get current chapter
    def get_current_chapter(self):
        return self._current_chapter
    
    def get_max_chapter(self):
        return self._max_chapter
    
    
    # write to file
    def write_java_file(self, user_code):
        self.set_working_directory_java()
        print("writing java code to file ...")
        try:
            f = open("Main.java","w")
            f.write(user_code)
            f.close()
            print("... code successfully written to file")
        except:
            print("... there was an error writing to file")
            
    def get_welcome_html(self):
        self.set_working_directory_tutorial()
        f = open("welcome.html","r", encoding='utf-8')
        welcome = f.read()
        f.close()
        return(welcome)
    
    def add_user(self, username, password):
        data = self.load_data()
        if username in data:
            return False  # Username already exists

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        data[username] = {"password_hash": password_hash, "assignment_chapter": 0,"current_chapter": 1, "preferences": 
            {"favorite_subjects": "", "hobbies": "", "profession": "", "other": ""}, "data": []}
        tutorial = data.get(username, {}).get("data", {})
        for i in range(1 , self._max_chapter + 1):
            java = self.get_original_java_file(i)
            assignment = self.get_original_assignment(i)
            tutorial.append({"chapter_nr": i, "assignment" : assignment, "java" : java})
        self.save_data(data)
        self.username = username
        self.new_user = True
        return True

    def authenticate_user(self, username, password):
        data = self.load_data()
        if username not in data:
            return False

        password_hash = data[username]["password_hash"]
        success = bcrypt.checkpw(password.encode(), password_hash.encode())
        if success :
            self.username = username
        return success

    def load_data(self):
        self.set_working_directory_tutorial()
        with self.json_user_path.open("r") as f:
            return json.load(f)

    def save_data(self, data):
        self.set_working_directory_tutorial()
        with self.json_user_path.open("w") as f:
            json.dump(data, f, indent=4)
    
    def load_user_data(self, username):
        data = self.load_data()
        return data.get(username, {}).get("data", {})

    def save_user_data(self, username, user_data):
        data = self.load_data()
        if username in data:
            data[username]["data"] = user_data
            self.save_data(data)
            
    def load_tutorial_data(self):
        self.set_working_directory_tutorial()
        with self.json_tutorial_path.open("r") as f:
            return json.load(f)