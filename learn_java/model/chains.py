import dotenv
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from PyQt6.QtCore import QThread
import re

import os
os.environ["OPENAI_API_KEY"] = "sk-proj-0KMQeINNnl2EU3f50CLVT3BlbkFJTJqRvYtm3xgqS95M4Hh3"


# Define chat model to use:
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Output parser to format the output of the LLM
output_parser = StrOutputParser()

# System role for the LLM    
system_role = """You are a friendly German speaking high school teacher for computer science that 
helps high school students to learn java. The student uses a program similar to an IDE. The gui of the program 
displays on the left hand side a tutorial with different chapters containing various topics of the java 
programming language. Each chapter also contains a corresponding assignment.
In the middle section of the gui is an editor in which the student can write java code to solve the assignment. 
The output of the program and hints are displayed in the right section. The student can compile and run his or her code 
with corresponding buttons. If applicable, the student can also enter input to the running program in the right section.
For most assignments the student is also given a starting code in the editor.""" 

system_role_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        template=system_role 
    )
)

# Load environment variables (mainly the token for the LLM)
#dotenv.load_dotenv()



class Chains:
    def __init__(self):
        super(Chains,self).__init__()    

    def compile_check(self, user_code, compile_result) -> str:
        
        system_compile_message = """You will be given the java code of the student and the error message of the compiler. 
        The student sees the error message of the compiler. 
        Analyze the java code and the error message. Then explain the relevant part of the error to the student. 
        Do not solve the problem for the student, but give him a hint that will guide him to the solution.
        
        error message: 
        {error}
        """
        
        system_compile_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["error"], template=system_compile_message 
            )
        )

        human_code_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["user_code"], template="""
                
                student code:
                {user_code}"""
            )
        )
        
        messages = [system_role_prompt, system_compile_message_prompt, human_code_prompt]
        prompt = ChatPromptTemplate(
            input_variables=["user_code", "error"],
            messages=messages,
        )
        chain = prompt | chat_model | output_parser

        return chain.invoke({"user_code": user_code, "error": compile_result})


    def run_check(self, user_code, assignment, output, topics, input) -> str:
        
        system_run_message = """You will be given the student's assignment, the java code of the student,
        all previous topics of the tutorial and the output of the program.
        If applicable, you will also be given the input to the program. 
        Analyze the assignment, the java code, the topics and the output and potential input. 
        Decide, whether the assignment was solved correctly. Be very generous with this decision. 
        Do not ask for things that are not specifically stated in the assignment.
        It is important that you do not ask for solutions that require knowledge not covered in the previous topics.
        If the assignment was solved correctly, only state this. Do not write anything further.
        If the assignment was not solved correctly, do not solve the problem for the student, 
        but give him a hint that will guide him to the solution.
        If the output is only correct for certain inputs, give a hint for different inputs 
        that lead to an incorrect output and thus show that the assignment was not solved correctly. 
        
        assignment: 
        {assignment}

        output:
        {output}

        previous topics:
        {topics}
        """
        
        system_run_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["assignment","output","topics"], template=system_run_message 
            )
        )

        human_code_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["user_code"], template="""
                
                student code:
                {user_code}"""
            )
        )

        if (input == ""):
            messages = [system_role_prompt, system_run_message_prompt, human_code_prompt]
            prompt = ChatPromptTemplate(
                input_variables=["assignment","output","topics","user_code"],
                messages=messages,
            )
        else:
            human_input_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["user_code"], template="""
                
                input:
                {input}"""
            )
            )
            messages = [system_role_prompt, system_run_message_prompt, human_code_prompt, human_input_prompt]
            prompt = ChatPromptTemplate(
            input_variables=["assignment","output","topics","user_code","input"],
            messages=messages,
            )
        
        chain = prompt | chat_model | output_parser

        return chain.invoke({"assignment": assignment,"output": output,"user_code": user_code, 
                             "topics": topics,"input": input})
    
    
    
class Assignment_Adjuster (QThread):
    def __init__(self,model):
        super(Assignment_Adjuster,self).__init__()
        self._running = True
        self._model = model
        
    def run(self):
        while self._running:
            chapter_nr = self.get_assignment_chapter() + 1
            if  chapter_nr < self._model.get_max_chapter():
                response = self.formulate_assignment(chapter_nr)
                self._model.set_assignment(chapter_nr=chapter_nr,assignment=response[0])
                self._model.set_java_file(chapter_nr=chapter_nr,code=response[1])
                self.set_assignment_chapter(chapter_nr)
                
            else:
                self._running = False
            
            
        
    def stop(self):
        self._running = False
        
    # get chapter number up to which the assignments have been adjusted
    def get_assignment_chapter(self):
        data = self._model.load_data()
        return data[self._model.username]['assignment_chapter']
    
    # set chapter number up to which the assignments have been adjusted
    def set_assignment_chapter(self,chapter_nr):
        data = self._model.load_data()
        data[self._model.username]['assignment_chapter'] = chapter_nr
        self._model.save_data(data)
        
    
    def formulate_assignment(self, chapter_nr) -> str:
        
        tutorial_chapter = self._model.get_tutorial_html(chapter_nr)
        assignment = self._model.get_original_assignment(chapter_nr)
        code = self._model.get_java_file(chapter_nr)
        topics = self._model.get_topics(chapter_nr)
                
        subject = self._model.get_favorite_subjects()
        hobby = self._model.get_hobbies()
        profession = self._model.get_profession()
        other = self._model.get_other()

        system_formulate_message = """You will be given the content of the current chapter
        and a corresponding assignment in html format. You will also be given the starting code for the student,
        all previous topics of the tutorial and a self-description of the student with his preferences. 
        Your task is to analyze the given information and reformulate the assignment and if necessary the starting code 
        in order to make the assignment more interesting for the student.
        It is important that you do not change the difficulty level and the extent of the assignment.
        Be aware that the starting code is only a starting point for the student and not the solution!
        Most of the time it contains a "todo ..." part. The revised version should contain this as well. 
        The new starting code should be of the same extent as the original starting code. 
        Give the assignment in html format and the starting code in plain text. 
        Wrap the html with ```html and ``` and the java code with ```java and ``` 

        chapter (in German):
        {tutorial_chapter}

        assignment (in German): 
        {assignment}

        starting code:
        {code}

        topics:
        {topics}
        """
        
        system_formulate_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["tutorial_chapter","assignment","code","topics"], template=system_formulate_message 
            )
        )

        human_preferences_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["subject","hobby","profession","other"], template="""
                
                preferences (in German):
                favorite subjects: {subject}
                hobbies: = {hobby}
                dream profession = {profession}
                additional information = {other}"""
            )
        )

        
        messages = [system_role_prompt, system_formulate_message_prompt, human_preferences_prompt]
        prompt = ChatPromptTemplate(
            input_variables=["tutorial_chapter","assignment","code","topics","subject","hobby","profession","other"],
            messages=messages,
        )
        
        
        chain = prompt | chat_model | output_parser

        response = chain.invoke({"tutorial_chapter": tutorial_chapter,"assignment": assignment,"code": code,"topics": topics,
                             "subject": subject,"hobby": hobby,"profession": profession,"other": other})
        
        
        keyword1 = ["`html","`java"]
        keyword2 = "`"

        start_pos = []
        extracted_text = []

        for i in range(2):
            # Find the start and end positions of the keywords
            start_pos.append(response.find(keyword1[i]) + len(keyword1[i]))
            end_pos = response.find(keyword2, start_pos[i])  # start searching for keyword2 after start_pos

            # Extract the text between the keywords
            extracted_text.append(response[start_pos[i]:end_pos])
        
        
        return(extracted_text)    
    