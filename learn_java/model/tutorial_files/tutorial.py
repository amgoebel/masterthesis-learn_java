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
        self._set_working_directory()
        filename = "chapter" + str(chapter) + ".html"
        path = self.file_path

        f = open(filename,"r")
        tutorial = f.read()
        f.close()
        return(tutorial)