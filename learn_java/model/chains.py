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
import re

class Chains:
    def __init__(self):
        super(Chains,self).__init__()
        dotenv.load_dotenv()
        
    chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    output_parser = StrOutputParser()
    
    system_role = """You are a friendly German speaking teacher that helps high school students to learn java.""" 
    
    system_role_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=system_role 
        )
    )

    def compile_check(self, user_code, compile_result) -> str:
        
        system_compile_message = """You will be given the java code of the student and the error message of the compiler. 
        The student does not see the error message of the compiler. 
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
        
        messages = [self.system_role_prompt, system_compile_message_prompt, human_code_prompt]
        prompt = ChatPromptTemplate(
            input_variables=["user_code", "error"],
            messages=messages,
        )
        chain = prompt | self.chat_model | self.output_parser

        return chain.invoke({"user_code": user_code, "error": compile_result})


    def run_check(self, user_code, assignment, output, topics, input) -> str:
        
        system_run_message = """You will be given the student's assignment, the java code of the student,
        all previous topics of the class and the output of the program.
        If applicable, you will also be given the input to the program. 
        Analyze the assignment, the java code, the topics and the output and potential input. 
        Decide, whether the assignment was solved correctly. Be very generous with this decision. 
        Do not ask for things that are not specifically stated in the assignment.
        It is important that you do not ask for solutions that require knowledge not covered in the previous topics.
        If the assignment was solved correctly, only state this. Do not write anything further.
        If the assignment was not solved correctly, do not solve the problem for the student, 
        but give him a hint that will guide him to the solution.
        If the output is only correct for certain inputs, give a hint for a different input 
        that leads to an incorrect output and thus shows that the assignment was not solved correctly. 
        
        assignment: 
        {assignment}

        output:
        {output}

        topics:
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
            messages = [self.system_role_prompt, system_run_message_prompt, human_code_prompt]
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
            messages = [self.system_role_prompt, system_run_message_prompt, human_code_prompt, human_input_prompt]
            prompt = ChatPromptTemplate(
            input_variables=["assignment","output","topics","user_code","input"],
            messages=messages,
            )
        
        chain = prompt | self.chat_model | self.output_parser

        return chain.invoke({"assignment": assignment,"output": output,"user_code": user_code, 
                             "topics": topics,"input": input})
    
    def formulate_assignment(self, tutorial_chapter, assignment, preferences, code, topics) -> str:
        
        name = preferences.get_name()
        age = preferences.get_age()
        subject = preferences.get_subject()
        hobby = preferences.get_hobby()
        profession = preferences.get_profession()
        role_model = preferences.get_role_model()

        system_formulate_message = """You will be given the content of the current chapter
        and a corresponding assignment in html format. You will also be given a starting code for the student,
        all previous topics of the class and preferences of the student. 
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
                input_variables=["name","age","subject","hobby","profession","role_model"], template="""
                
                preferences (in German):
                name: {name}
                age: {age}
                favorite subject: {subject}
                hobbys: = {hobby}
                dream profession = {profession}
                role_model = {role_model}"""
            )
        )

        
        messages = [self.system_role_prompt, system_formulate_message_prompt, human_preferences_prompt]
        prompt = ChatPromptTemplate(
            input_variables=["tutorial_chapter","assignment","code","topics","name","age","subject","hobby","profession","role_model"],
            messages=messages,
        )
        
        
        chain = prompt | self.chat_model | self.output_parser

        response = chain.invoke({"tutorial_chapter": tutorial_chapter,"assignment": assignment,"code": code,"topics": topics,
                             "name": name,"age": age,"subject": subject,"hobby": hobby,"profession": profession,"role_model": role_model})
        
        
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