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
        Analyse the java code and the error message. Then explain the relevant part of the error to the student. 
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
                input_variables=["code"], template="""
                
                student code:
                {code}"""
            )
        )
        
        messages = [self.system_role_prompt, system_compile_message_prompt, human_code_prompt]
        prompt = ChatPromptTemplate(
            input_variables=["code", "error"],
            messages=messages,
        )
        chain = prompt | self.chat_model | self.output_parser

        return chain.invoke({"code": user_code, "error": compile_result})

