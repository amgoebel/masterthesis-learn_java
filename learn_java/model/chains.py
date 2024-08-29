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


    def run_check(self, user_code, assignment, output, input=None) -> str:
        
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
        output command
        """
        
        system_run_message_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["assignment","output"], template=system_run_message 
            )
        )

        human_code_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["user_code"], template="""
                
                student code:
                {user_code}"""
            )
        )

        if (input == None):
            messages = [self.system_role_prompt, system_run_message_prompt, human_code_prompt]
            prompt = ChatPromptTemplate(
                input_variables=["assignment","output","user_code"],
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
            input_variables=["assignment","output","user_code","input"],
            messages=messages,
            )
        
        chain = prompt | self.chat_model | self.output_parser

        return chain.invoke({"assignment": assignment,"output": output,"user_code": user_code, "input": input})