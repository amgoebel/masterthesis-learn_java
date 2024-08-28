import subprocess
import threading

class Java_Engine(threading.Thread):
    def __init__(self, model, communicator):
        super(Java_Engine,self).__init__()
        self._model = model
        self._process = None
        self._input_monitor = None
        self._output_monitor = None
        self._communicator = communicator
        
    # run java code
    def run(self):
        self._model.set_working_directory()
        print("running java program ...")
        self._process = subprocess.Popen(['java', 'main'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                bufsize=1)

        self._input_monitor = Input_Monitor(process=self._process,model=self._model)
        self._output_monitor = Output_Monitor(process=self._process,model=self._model)
        self._input_monitor.start()
        self._output_monitor.start()
        self._output_monitor.join()
        self._input_monitor.join()
        self._communicator.java_program_stopped.emit()
        print("... java program has terminated")

    def stop(self):
        self._process.kill()
        self._output_monitor.join()
        self._input_monitor.join()
        


class Output_Monitor(threading.Thread):
    def __init__(self, process, model):
        super(Output_Monitor,self).__init__()
        self._process = process
        self._model = model
        self._running = True

    def run(self):
        self._model.clear_output()
        total_output = ""
        while self._running:
            if(self._process.poll() != None):
                self._running = False
                break
            output = self._process.stdout.read(1)
            if output:
                total_output += output
                self._model.update_output(total_output)

    def stop(self):
        self.running = False 

class Input_Monitor(threading.Thread):
    def __init__(self, process, model):
        super(Input_Monitor,self).__init__()
        self._process = process
        self._model = model
        self._running = True

    def run(self):
        while self._running:
            if(self._process.poll() != None):
                self._running = False
                break
            if self._model.get_input_sent():
                self._model.set_input_sent(False)
                self._process.stdin.write(self._model.get_input() + "\n")
                self._process.stdin.flush()

    def stop(self):
        self.running = False 