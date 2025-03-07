# This python file creates a new chapter in the file tutorial.json.
# The file tutorial.json needs to be in the same directory as this python file.
# The new chapter consists of a tutorial, an assignment and a starting java code.
# The topic of the chapter needs to be stated in tutorial.json at the corresponding chapter number.
# It is highly recommended that some chapters already exist in tutorial.json as an example for the LLM

# Choose the chapter number to be added and the LLM to be used (lines 33 to 37)

# choose the chapter number here:
chapter_number = 9




import dotenv
import os

# LLMS:
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (mainly the token for the LLM)
dotenv.load_dotenv()

# Define chat model to use: (comment out the others)
#chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chat_model = ChatOpenAI(model="gpt-4o", temperature=0)
#chat_model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
#chat_model = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)

# Output parser to format the output of the LLM
output_parser = StrOutputParser()

# System role for the LLM 
system_role = """You are a German speaking high school teacher for computer science that develops chapters for
    a java learn course for beginners. Each chapter also contains an assignment in the end.
    The course is being used in an IDE which is divided into three sections. In the left section the content
    of the chapter is displayed. In the middle section is an editor in which the student can write java code
    to solve the assignment. The output of the program and hints are displayed in the right section. The student 
    can compile and run its code with corresponding buttons. If applicable, the student can also enter input 
    to the running program in the right section.
    For most assignments the student is also given a starting code in the editor.
    Your assignment is to create a specific chapter, the corresponding assignment and a java code as the 
    starting code. You can reference the starting code in the chapter since the student can see both."""

system_role_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template=system_role
    )
)


def create_tutorials(json_file, chapter) -> str:
    # Create tutorial for the given chapter including assignment and starting starting code.

    system_create_tutorial_message = """You will be given a json file that contains three keys: "tutorial",
    "html_head" and "html_tail".
    The value of "tutorial" is an array where each element corresponds to a chapter and contains five keys: 
    "chapter_nr": The number of the chapter, "topic": The topic of the chapter, "content": 
    The content of the chapter as an html body, "assignment": The assignment in the end of the chapter as an 
    html body and "java": The starting code for the student.
    The values of "html_head" and "html_tail" are later placed around the values of "content" and "assignment"
    in order to build a valid html document.
    Some chapters are already finished and can be used as examples of how a chapter should look like 
    together with the corresponding assignment and starting java code. 
    Closely analyze the examples and create values for all keys of chapter nr {chapter}. Make sure that the 
    chapter is similar to the examples in style and extensiveness and that the chapter does not anticipate 
    content of later chapters.
    It is import that you keep in mind, that the student only knows the content of the previous 
    chapters and has no other programming experience. This also means that the student does not know
    technical terms such as "class", "method", "declaration" or "initialization". You have to explain 
    technical terms when you introduce them and you can only use them after they have been introduced.
    It is also important that the starting code does not solve the assignment. It only gives 
    a rudimentary starting frame. Write "to do ... " into the starting code where the students has 
    to add his or her code.
        
    Give the entire JSON file with all its original content enhanced with the added chapter.
    Wrap the file with ```json and ``` 
    """

    system_create_tutorial_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["chapter"], template=system_create_tutorial_message
        )
    )
    
    human_tutorial_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["json_file"], template="""
            
            JSON file:
            {json_file}            
       
            """
        )
    )

    messages = [system_role_prompt, system_create_tutorial_prompt,human_tutorial_prompt]
    prompt = ChatPromptTemplate(
        input_variables=["json_file", "chapter"],
        messages=messages,
    )
    chain = prompt | chat_model | output_parser

    response = chain.invoke(
        {"json_file": json_file, "chapter": chapter})

    keyword1 = "```json"
    keyword2 = "```"

       
    # Find the start and end positions of the keywords
    start_pos = response.find(keyword1) + len(keyword1)
    end_pos = response.find(keyword2, start_pos)  # start searching for keyword2 after start_pos
    
    # Extract the text between the keywords
    extracted_text = response[start_pos:end_pos]

    return(extracted_text)



def set_working_directory():
    # set the correct working directory
    try:
        os.chdir(os.path.dirname(__file__))
    except:
        print("... there was an error setting the working directory")


def get_json_file():
    # load content from tutorial file
    filename = "tutorial.json"
    f = open(filename, "r", encoding='utf-8')
    file_content = f.read()
    f.close()
    return (file_content)


def save_file(content):
    # write new content to tutorial file
    filename = "tutorial.json"
    f = open(filename, "w", encoding='utf-8')
    f.write(content)
    f.close


def main():
    # main program
    set_working_directory()
    json_file = get_json_file()
    response = create_tutorials(chapter=chapter_number,json_file=json_file)
    save_file(response)
        
        
if (__name__ == "__main__"):
    main()