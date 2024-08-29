import os

class Tutorial_Handling:
    def __init__(self):
        super(Tutorial_Handling,self).__init__()
        self.file_path = os.path.dirname(__file__)

    def _set_working_directory(self):
        try:
            os.chdir(self.file_path)
        except:
            print("... there was an error setting the working directory")
    
    def get_tutorial_html(self,chapter):
        assignment = self.get_assignment(chapter)
        assignment = assignment.replace("<","&lt;")
        assignment = assignment.replace(">","&gt;")
        filename = "chapter" + str(chapter) + ".html"
        path = self.file_path

        f = open(filename,"r")
        tutorial = f.read()
        f.close()

        tutorial = tutorial.replace("{assignment}",assignment)
        return(tutorial)
    
    def get_assignment(self,chapter):
        self._set_working_directory()
        filename = "assignment" + str(chapter) + ".txt"
        path = self.file_path

        f = open(filename,"r")
        assignment = f.read()
        f.close()
        return(assignment)
    
    def get_topics(self,chapter):
        self._set_working_directory()
        filename = "topics" + str(chapter) + ".txt"
        path = self.file_path

        f = open(filename,"r")
        topics = f.read()
        f.close()
        return(topics)