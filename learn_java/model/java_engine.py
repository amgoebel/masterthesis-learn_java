from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
import os
import subprocess

class Java_Engine(QThread):
    stop_signal = pyqtSignal()

    def __init__(self, model, communicator):
        super(Java_Engine, self).__init__()
        self._model = model
        self._process = None
        self._input_monitor = None
        self._output_monitor = None
        self._communicator = communicator
        self.stop_signal.connect(self.stop)

    # Run Java code
    def run(self):
        self._model.set_working_directory_java()
        print("running java program ...")
        self._process = subprocess.Popen(
            ['java', 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        self._input_monitor = Input_Monitor(process=self._process, model=self._model)
        self._output_monitor = Output_Monitor(process=self._process, model=self._model)
        self._input_monitor.start()
        self._output_monitor.start()

        # Wait for the monitors to finish
        self._output_monitor.wait()
        self._input_monitor.wait()
        self._communicator.java_program_stopped.emit()

        stderr = str(self._process.communicate())
        if self._process.returncode != 0:
            self._model.update_output("Fehlermeldung:\n" + stderr)
        print("... java program has terminated")

    @pyqtSlot()
    def stop(self):
        if self._process:
            self._process.kill()
        if self._output_monitor:
            self._output_monitor.stop()
        if self._input_monitor:
            self._input_monitor.stop()


class Output_Monitor(QThread):
    data_signal = pyqtSignal(str)  # Signal to send data to the main thread

    def __init__(self, process, model):
        super(Output_Monitor, self).__init__()
        self._process = process
        self._model = model
        self._running = True

        # Connect signal to model update
        self.data_signal.connect(self._model.update_output)

    def run(self):
        self._model.clear_output()
        total_output = ""
        while self._running:
            if self._process.poll() is not None:
                self._running = False
                break
            output = self._process.stdout.read(1)
            if output:
                total_output += output
                self.data_signal.emit(total_output)  # Emit signal instead of direct update

    def stop(self):
        self._running = False


class Input_Monitor(QThread):
    def __init__(self, process, model):
        super(Input_Monitor, self).__init__()
        self._process = process
        self._model = model
        self._running = True

    def run(self):
        while self._running:
            if self._process.poll() is not None:
                self._running = False
                break
            if self._model.get_input_sent():
                self._model.set_input_sent(False)
                self._process.stdin.write(self._model.get_input() + "\n")
                self._process.stdin.flush()

    def stop(self):
        self._running = False
        

# compile java code
def compile_java():
    set_working_directory_java()
    print("starting compilation ...")
    try:
        p = subprocess.run(["javac","Main.java"], capture_output=True, text=True, check=True)
        print("... compilation successful")
        error_code = "compilation successful"
    except subprocess.CalledProcessError as e: 
        print("... compilation failed")
        print("Error message: ", e.stderr)
        error_code = "Error message: " + e.stderr
    return(error_code)

# change working directory
def set_working_directory_java():
    file_path = os.path.dirname(__file__)
    try:
        os.chdir(file_path + "/java_files")
    except:
        print("... there was an error setting the working directory")