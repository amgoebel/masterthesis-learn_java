import uuid
import dotenv

# LLMS:
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory
from PyQt6.QtCore import QThread


# Define chat model to use: (comment out the others)
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#chat_model = ChatOpenAI(model="gpt-4o", temperature=0)
#chat_model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
#chat_model = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0)

# Output parser to format the output of the LLM
output_parser = StrOutputParser()

# System role for the LLM    
system_role = """You are a friendly German speaking high school teacher for computer science that 
helps high school students to learn java. Always answer in German. The student uses a program similar to an IDE. The gui of the program 
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
dotenv.load_dotenv()

class Chains:
    # Class to handle interactions with the language model for compilation and execution checks.
    def __init__(self):
        # Initialize the Chains class.
        super(Chains,self).__init__()    

    def compile_check(self, user_code, compile_result) -> str:
        # Check the compilation result and provide hints to the user based on the error message.
        
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
        # Check the execution result and provide hints to the user based on the program output.
        
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
    # Thread class to adjust assignments based on user preferences. (runs in the background)
    def __init__(self,model):
        # Initialize the assignment adjuster with the model.
        super(Assignment_Adjuster,self).__init__()
        self._running = True
        self._model = model
        
    def run(self):
        # Run the assignment adjustment process for each chapter.
        while self._running:
            chapter_nr = self.get_assignment_chapter() + 1
            if  chapter_nr < self._model.get_max_chapter() + 1:
                response = self.formulate_assignment(chapter_nr)
                self._model.set_assignment(chapter_nr=chapter_nr,assignment=response[0])
                self._model.set_java_code(chapter_nr=chapter_nr,code=response[1])
                self.set_assignment_chapter(chapter_nr)
                print(f"Chapter {chapter_nr} has been adjusted to the users preferences.")
                
            else:
                self._running = False
                print("All chapters have been adjusted to the users preferences.")  
        
    def stop(self):
        # Stop the assignment adjustment process.
        self._running = False
        
    def get_assignment_chapter(self):
        # Get the chapter number up to which assignments have been adjusted.
        data = self._model.load_user_data()
        return data['assignment_chapter']
    
    def set_assignment_chapter(self,chapter_nr):
        # Set the chapter number up to which assignments have been adjusted.
        data = self._model.load_user_data()
        data['assignment_chapter'] = chapter_nr
        self._model.save_user_data(data)
        
    def formulate_assignment(self, chapter_nr) -> str:
        # Formulate a new assignment and starting code based on user preferences.
        
        tutorial_chapter = self._model.get_tutorial_html(chapter_nr,12)
        assignment = self._model.get_original_assignment(chapter_nr)
        code = self._model.get_original_java_code(chapter_nr)
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
        Do not give the chapter, only the assignment and the starting code. 
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
    
    
class Chat_Bot_Compile (QThread):
    # Thread class to handle chat bot interactions for code compilation errors.
    
    def __init__(self,model,communicator,user_code,compile_result,initial_response):
        # Initialize the chat bot for compilation with the model, communicator, and initial data.
        super(Chat_Bot_Compile,self).__init__()
        self._running = True
        self._model = model
        self._communicator = communicator
        self._user_code = user_code
        self._compile_result = compile_result
        self._initial_response = initial_response
          
    
    def run(self):
        # Run the chat bot to handle user questions about compilation errors.
        
        store = {}  # In-memory store for session histories

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            # Function to manage session history
            if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()
            return store[session_id]

        # Define the system and user prompt templates
        system_compile_chat_message = """You will be given the java code of the student and the error message of the compiler. 
        The student sees the error message of the compiler.
        You have already analyzed the code and the error and have given him a corresponding initial hint.
        Your task is to answer follow-up questions by the student about the error and your analysis. Only answer questions 
        concerning this and do not solve the problem for the student, but give him a further hint that will guide him to the 
        solution.

        error message: 
        {error}

        java code:
        {user_code}

        initial hint:
        {hint}
        """

        # Prompt for the system message
        system_compile_message_chat_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["error", "user_code", "hint"], 
                template=system_compile_chat_message
            )
        )
        
        # Prompt for the user question
        user_question_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{question}")
        )

        # Define the full chat prompt template
        chat_prompt = ChatPromptTemplate(
            messages=
            [
                system_compile_message_chat_prompt,  # The system message
                MessagesPlaceholder(variable_name="messages"),  # Placeholder for dynamic history
                user_question_prompt,  # The current user message
            ]
        )

        # Create the chain with system and user prompt
        chain = chat_prompt | chat_model

        # Add message history management
        with_message_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_session_history,
            input_messages_key="messages",  # Key for historical messages
        )

        # Config for the session
        session_id = str(uuid.uuid4())
        config = {"configurable": {"session_id": session_id}}

        # Main loop for chat
        while self._running:            
            if self._model.get_question_sent():
                self._model.set_question_sent(False)
                user_input = self._model.get_question()
                # Invoke the chain with user input and session configuration
                response = with_message_history.invoke(
                    {"question": user_input, "messages": [],
                    "error": self._compile_result,
                    "user_code": self._user_code,
                    "hint": self._initial_response},  # Pass user input and empty initial history
                    config=config,
                )
                self._model.set_answer(response.content)
                 # Sent signal to controller that answer has been submitted
                self._communicator.answer_sent.emit()            
                      
    def stop(self):
        # Stop the chat bot.
        self._running = False
        
        
class Chat_Bot_Run (QThread):
    # Thread class to handle chat interactions for code execution results.
    
    def __init__(self,model,communicator,user_code,assignment,topics,input,output,initial_response):
        # Initialize the chat bot for execution with the model, communicator, and initial data.
        super(Chat_Bot_Run,self).__init__()
        self._running = True
        self._model = model
        self._communicator = communicator
        self._assignment = assignment
        self._user_code = user_code
        self._topics = topics
        self._input = input
        self._output = output
        self._initial_response = initial_response
          
    def run(self):
        # Run the chat bot to handle user questions about execution results.      
        
        store = {}   # In-memory store for session histories
        
        # Function to manage session history
        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()
            return store[session_id]

        # Define the system and user prompt templates
        system_run_chat_message = """You will be given the student's assignment, the java code of the student,
        all previous topics of the tutorial and the output of the program.
        If applicable, you will also be given the input to the program.
        You have already analyzed the code, the topics and potential input and have given him a corresponding initial hint.
        Your task is to answer follow-up questions by the student about your analysis. Only answer questions 
        concerning this and do not solve the problem for the student, but give him a further hint that will guide him to the 
        solution. If applicable you can reevaluate your analysis and tell the student that the assignment was solved correctly.
        
        assignment: 
        {assignment}

        java code:
        {user_code}
        
        potential input:
        {input}
                
        output:
        {output}

        previous topics:
        {topics}

        initial hint:
        {hint}
        """

        # Prompt for the system message
        system_run_message_chat_prompt = SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=["assignment","user_code","input","output","topics","hint"], 
                template=system_run_chat_message
            )
        )
        
        # Prompt for the user question
        user_question_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template="{question}")
        )

        # Define the full chat prompt template
        chat_prompt = ChatPromptTemplate(
            messages=
            [
                system_run_message_chat_prompt,  # The system message
                MessagesPlaceholder(variable_name="messages"),  # Placeholder for dynamic history
                user_question_prompt,  # The current user message
            ]
        )

        # Create the chain with system and user prompt
        chain = chat_prompt | chat_model

        # Add message history management
        with_message_history = RunnableWithMessageHistory(
            runnable=chain,
            get_session_history=get_session_history,
            input_messages_key="messages",  # Key for historical messages
        )

        # Config for the session
        session_id = str(uuid.uuid4())
        config = {"configurable": {"session_id": session_id}}

        # Main loop for chat
        while self._running:            
            if self._model.get_question_sent():
                self._model.set_question_sent(False)
                user_input = self._model.get_question()
                # Invoke the chain with user input and session configuration
                response = with_message_history.invoke(
                    {"question": user_input, "messages": [],
                    "assignment": self._assignment,
                    "user_code": self._user_code,
                    "input": self._input,
                    "output": self._output,
                    "topics": self._topics,   
                    "hint": self._initial_response},  # Pass user input and empty initial history
                    config=config,
                )
                self._model.set_answer(response.content)
                 # Sent signal to controller that answer has been submitted
                self._communicator.answer_sent.emit()            
                      
    def stop(self):
        # Stop the chat bot.
        self._running = False