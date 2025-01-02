import os
import sys
import json
import threading
import bcrypt
import base64
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.fernet import Fernet
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QCoreApplication

# Thread lock to handle file access in a thread-safe manner
file_lock = threading.Lock()

class Handling(QAbstractListModel):
    # Handles data and user interactions
    def __init__(self):
        super(Handling,self).__init__()
        
        # Paths to data files (user and tutorial data)
        self.json_user_path = Path("users.json")   # encrypted
        self.json_tutorial_path = Path("tutorial.json")  # fixed and not encrypted
        
        # Determine file path based on execution mode (executable or script)
        if getattr(sys, 'frozen', False):
            self.file_path = os.path.dirname(sys.executable)
        elif __file__:
            self.file_path = os.path.dirname(__file__) 
        
        # Initialize instance variables
        self.username = ""               # Current username
        self.password = ""               # Current user password
        self.fernet = ""                 # Encryption object for user data
        self.new_user = False            # Flag for new user creation
        self._current_chapter = 1        # Tracks the current tutorial chapter
        self._max_chapter = 25           # Maximum number of chapters
        self._output = ""                # Output from Java program
        self._input = ""                 # Input for Java program
        self._input_sent = False         # Flag for input sent status
        self._question = ""              # Chatbot question
        self._question_sent = False      # Flag for chatbot question sent status
        self._answer = ""                # Chatbot answer

    ### Output handling of the running java program (needed for the QAbstractListModel):
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._output)
        return None
    
    def setData(self, index, output, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._output = output
            self.dataChanged.emit(index, index)   # Notify view about data change
            QCoreApplication.processEvents()      # Process GUI events
            return True
        return False

    def update_output(self, output):
        # Update output data
        self.setData(self.index(0), output)

    def get_output(self):
        # Retrieve current output
        return(self.data(self.index(0)))
    
    def clear_output(self):
        # Clear program output
        self.update_output("")   

    def rowCount(self, index=QModelIndex()):
        # Define row count (single row), needed for the QAbstractListModel 
        return 1
    
    ### Input handling for Java program:
    def set_input(self,input):
        # Set input for Java program
        self._input = input
        self.set_input_sent(True)

    def get_input(self):
        # Get the current input
        return self._input  

    def set_input_sent(self,value):
        # Set the input sent status
        self._input_sent = value 

    def get_input_sent(self):
        # Check if input has been sent
        return self._input_sent
    
    ### Chat bot handling (question and answer):
    def set_question(self,question):
        # Set the chatbot question
        self._question = question
        self.set_question_sent(True)

    def get_question(self):
        # Get the chatbot question
        return self._question

    def set_question_sent(self,value):
        # Set question sent status
        self._question_sent = value

    def get_question_sent(self):
        # Check if question has been sent
        return self._question_sent

    def set_answer(self,answer):
        # Set the chatbot answer
        self._answer = answer

    def get_answer(self):
        # Get the chatbot answer
        return self._answer

    ### Java code handling for each chapter:
    def get_java_code(self,chapter_nr):
        # Retrieve Java code for a specific chapter
        data = self.load_user_data()
        text = data.get("tutorial", {})[chapter_nr - 1]['java']
        return text

    def set_java_code(self,chapter_nr,code):
        # Save Java code for a specific chapter
        data = self.load_user_data()     
        data.get("tutorial", {})[chapter_nr - 1]['java'] = code
        self.save_user_data(data)

    def get_current_java_code(self):
        # Retrieve Java code for the current chapter
        data = self.load_user_data()      
        text = data.get("tutorial", {})[self._current_chapter - 1]['java']
        return text

    def set_current_java_code(self,code):
        # Save Java code for the current chapter
        data = self.load_user_data()
        data.get("tutorial", {})[self._current_chapter - 1]['java'] = code
        self.save_user_data(data)

    def get_original_java_code(self,chapter_nr):
        # Load the original Java code (not adjusted for the user)
        data = self.load_tutorial_data()
        text = data['tutorial'][chapter_nr - 1]['java']
        return text
    
    # Write Java code to file for execution
    def write_java_file(self, user_code):
        # Writes java code to the file Main.java
        self.set_working_directory_java()
        print("writing java code to file ...")
        try:
            f = open("Main.java","w", encoding='utf-8')
            f.write(user_code)
            f.close()
            print("... code successfully written to file")
        except:
            print("... there was an error writing to file")
    
    ### Tutorial file handling:        
    def get_tutorial_html(self,chapter_nr,font_size):
        # Load the tutorial of a specific chapter in a specific font size
        data = self.load_tutorial_data()
        data2 = self.load_user_data().get("tutorial", {})
        text = data['html_head']
        fsize = str(font_size) + "pt"
        text = text.replace('fsize',fsize)
        text += data['tutorial'][chapter_nr - 1]['content']
        text += data2[chapter_nr - 1]['assignment']
        text += data['html_tail']
        return text
    
    def get_assignment(self,chapter_nr):
        # Load the assignment of a specific chapter
        data = self.load_user_data()
        text = data.get("tutorial", {})[chapter_nr - 1]['assignment']
        return text  
    
    def set_assignment(self,chapter_nr,assignment):
        # Set the assignment of a specific chapter (after adjusting it to the user)
        data = self.load_user_data()       
        data.get("tutorial", {})[chapter_nr - 1]['assignment'] = assignment
        self.save_user_data(data)
        
    def get_original_assignment(self,chapter_nr):
        # Load the original assignment of a specific chapter (not adjusted for the user)
        data = self.load_tutorial_data()        
        text = data['tutorial'][chapter_nr - 1]['assignment']
        return text
    
    def get_topics(self,chapter_nr):
        # Load the topics of the tutorial up to a specific chapter (for the LLM know the context)
        data = self.load_tutorial_data()        
        text = "topics:"+"\n"
        for chapter in range(chapter_nr):
            text += data['tutorial'][chapter]['topic'] + "\n"
        return text
    
    ### Chapter handling:
    def set_current_chapter(self,chapter):
        # Set the the current chapter to a specific chapter
        self._current_chapter = chapter
    
    def get_current_chapter(self):
        # Load the current chapter
        return self._current_chapter
    
    def get_max_chapter(self):
        # Load the number of chapters
        return self._max_chapter
        
    def set_starting_chapter(self):
        # Set the chapter at the start of the program from last session
        self._current_chapter = self.load_user_data()['current_chapter']
       
    def set_session_chapter(self):
        # Set current chapter for the start of the next session 
        data = self.load_user_data()
        data["current_chapter"] = self._current_chapter
        self.save_user_data(data)
        
    ### User preferences handling:
    def set_preferences(self, favorite_subjects, hobbies,profession, other):
        # Save the user's preferences (for adjusting the assignments)
        data = self.load_user_data()
        data['preferences']['set'] = True
        data['preferences']['favorite_subjects'] = favorite_subjects
        data['preferences']['hobbies'] = hobbies
        data['preferences']['profession'] = profession
        data['preferences']['other'] = other
        self.save_user_data(data)
        
    def get_preferences_set(self):
        # Check if the user's preferences have been set
        data = self.load_user_data()
        return data['preferences']['set']
    
    def set_preferences_set(self):
        # Set preferences set status
        data = self.load_user_data()
        data['preferences']['set'] = True
        self.save_user_data(data)
    
    def get_favorite_subjects(self):
        # Load the user's favorite subject
        data = self.load_user_data()
        return data['preferences']['favorite_subjects']
    
    def get_hobbies(self):
        # Load the user's hobbies
        data = self.load_user_data()
        return data['preferences']['hobbies']
    
    def get_profession(self):
        # Load the user's dream profession
        data = self.load_user_data()
        return data['preferences']['profession']
    
    def get_other(self):
        # Load the user's additional information
        data = self.load_user_data()
        return data['preferences']['other']    
    
    ### User management:
    def add_user(self, username, password):
        # Add a new user with encrypted data and default settings
        data = self.load_data()
        if username in data:
            return False  # Username already exists

        # Generate password hash and encryption key
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        salt = os.urandom(16)
        
        # Create encryption key and initialize user data
        self.fernet = Fernet(self.derive_key(password, salt))
        data[username] = {
            "password_hash": password_hash,
            "salt": base64.urlsafe_b64encode(salt).decode(),  # Store the salt as a string
            "user_data": {
                "assignment_chapter": 0,
                "current_chapter": 1,
                "preferences": {
                    "set": False,
                    "favorite_subjects": "",
                    "hobbies": "",
                    "profession": "",
                    "other": "",
                },
                "tutorial": [],
            },
        }
        
        # Prepare tutorial data for each chapter
        tutorial = data.get(username, {}).get("user_data", {}).get("tutorial", {})
        for i in range(1 , self._max_chapter + 1):
            java = self.get_original_java_code(i)
            assignment = self.get_original_assignment(i)
            tutorial.append({"chapter_nr": i, "assignment" : assignment, "java" : java})

        # Encrypt and save user data
        user_data_json = json.dumps(data[username]["user_data"])
        encrypted_data = self.fernet.encrypt(user_data_json.encode())
        data[username]["user_data"] = encrypted_data.decode()
        self.save_data(data)
        
        self.username = username
        self.password = password
        self.new_user = True       # Set flag for new user
        return True

    def authenticate_user(self, username, password):
        # Authenticate user credentials
        data = self.load_data()
        if username not in data:
            return False          # Username does not exist

        # Verify password hash and initialize encryption key
        password_hash = data[username]["password_hash"]
        success = bcrypt.checkpw(password.encode(), password_hash.encode())
        if success :
            self.username = username
            self.password = password
            salt = base64.urlsafe_b64decode(data[username]["salt"])
            self.fernet = Fernet(self.derive_key(password, salt))
        return success                # Username and password are correct

    def derive_key(self,password: str, salt: bytes) -> bytes:
        # Derive an encryption key using PBKDF2 and SHA256
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,  # Key length for Fernet
            salt=salt,
            iterations=100_000,  # Number of iterations (adjust for security/performance)
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    ### File handling: 
    def load_data(self):
        # Load user data from JSON file
        self.set_working_directory_tutorial()
        with file_lock:
            with self.json_user_path.open("r", encoding="utf-8") as f:
                return json.load(f)
    
    def load_tutorial_data(self):
        # Load tutorial data from JSON file
        self.set_working_directory_tutorial()
        with self.json_tutorial_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self, data):
        # Save user data to JSON file
        self.set_working_directory_tutorial()
        with file_lock:
            with self.json_user_path.open("w") as f:
                json.dump(data, f, indent=4)
    
    def load_user_data(self):
        # Load and decrypt user-specific data
        data = self.load_data()
        encrypted_user_data = data[self.username]["user_data"]
        decrypted_data = self.fernet.decrypt(encrypted_user_data.encode()).decode()
        user_data = json.loads(decrypted_data)  # Convert back to dictionary
        return user_data
        
    def save_user_data(self, user_data):
        # Encrypt and save user-specific data
        data = self.load_data()
        user_data_json = json.dumps(user_data)
        encrypted_data = self.fernet.encrypt(user_data_json.encode())
        data[self.username]["user_data"] = encrypted_data.decode()
        self.save_data(data)

    def set_working_directory_java(self):
        # Set working directory for Java files
        try:
            os.chdir(self.file_path + "/java_files")
        except:
            print("... there was an error setting the working directory")
            
    def set_working_directory_tutorial(self):
        # Set working directory for tutorial files
        try:
            os.chdir(self.file_path + "/tutorial_files")
        except:
            print("... there was an error setting the working directory")