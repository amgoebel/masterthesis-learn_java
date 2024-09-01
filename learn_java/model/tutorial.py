import os

class Tutorial_Handling:
    def __init__(self):
        super(Tutorial_Handling,self).__init__()
        self.file_path = os.path.dirname(__file__)

    def _set_working_directory(self):
        try:
            os.chdir(self.file_path + "/tutorial_files")
        except:
            print("... there was an error setting the working directory")
    
    def get_welcome_html(self):
        self._set_working_directory()
        f = open("welcome.html","r", encoding='utf-8')
        welcome = f.read()
        f.close()
        return(welcome)
    
    def get_tutorial_html(self,chapter):
        assignment = self.get_assignment(chapter)
        filename = "chapter" + str(chapter) + ".html"

        f = open(filename,"r", encoding='utf-8')
        tutorial = f.read()
        f.close()

        tutorial = tutorial + assignment
        return(tutorial)
    
    def get_assignment(self,chapter):
        self._set_working_directory()
        filename = "assignment" + str(chapter) + ".html"
        
        f = open(filename,"r", encoding='utf-8')
        assignment = f.read()
        f.close()
        return(assignment)
    
    def get_topics(self,chapter):
        self._set_working_directory()
        filename = "topics" + str(chapter) + ".txt"
        path = self.file_path

        f = open(filename,"r", encoding='utf-8')
        topics = f.read()
        f.close()
        return(topics)