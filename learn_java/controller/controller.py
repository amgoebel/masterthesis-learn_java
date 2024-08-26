from model.java_engine import Java_Engine

class Controller:
    """Learn Java's controller class."""

    def __init__(self, model, view):
        super(Controller,self).__init__()
        self._model = model
        self._view = view
        self._java_engine = None
        self._connectSignalsAndSlots()
        self._set_initial_values()

    def _connectSignalsAndSlots(self):
        self._view.pB_compile.clicked.connect(self._compile_java_code)
        self._view.pB_run.clicked.connect(self._run_java_program)
        self._view.pB_send.clicked.connect(self._send_input)
        self._view.lE_input.returnPressed.connect(self._send_input)

    def _set_initial_values(self):
        self._view.pTE_code.setPlainText(self._model.get_current_java_file())

    def _update_output(self, output, colorNr=0):
        self._model.update_output(output,colorNr)

    def _send_input(self):
        self._model.set_input(self._view.lE_input.text())
        self._view.lE_input.clear()
        
    def _compile_java_code(self):
        user_code = self._view.pTE_code.toPlainText()
        self._model.write_java_file(user_code)
        compile_result = self._model.compile_java()
        if (compile_result == "compilation successful"):
            colorNr = 1
            self._view.pB_run.setEnabled(True)
            compile_result = """Das kompilieren deines Codes hat geklappt.
Mit der Taste "start" kannst du dein Programm nun laufen lassen.""" 
        else:
            colorNr = 2
            self._view.pB_run.setEnabled(False)
            compile_result = self._model.compile_check(user_code=user_code,compile_result=compile_result)    
        self._update_output(compile_result,colorNr)

    def _run_java_program(self):
        self._java_engine = Java_Engine(self._model)
        self._java_engine.start()