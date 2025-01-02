from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot
import os
import subprocess
import sys

# Determine OS-specific options
if sys.platform == "win32":  # Windows
    creation_flags = subprocess.CREATE_NO_WINDOW
else:  # Linux or others
    creation_flags = 0  # No special flags needed

class Java_Engine(QThread):
    # Thread class to run and manage the execution of Java programs.
    stop_signal = pyqtSignal()

    def __init__(self, model, communicator):
        # Initialize the Java engine with the model and communicator.
        super(Java_Engine, self).__init__()
        self.model = model
        self.process = None
        self.input_monitor = None
        self.output_monitor = None
        self.communicator = communicator
        self.stop_signal.connect(self.stop)

    def run(self):
        # Run the Java program and manage input/output monitoring.
        self.model.set_working_directory_java()
        print("running java program ...")
        self.process = subprocess.Popen(
            ['java', 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,
            universal_newlines=True,
            creationflags=creation_flags
        )

        self.input_monitor = Input_Monitor(process=self.process, model=self.model)
        self.output_monitor = Output_Monitor(process=self.process, model=self.model)
        self.input_monitor.start()
        self.output_monitor.start()

        # Wait for the monitors to finish
        self.output_monitor.wait()
        self.input_monitor.wait()
        self.communicator.java_program_stopped.emit()

        #stderr = str(self._process.communicate())
        stderr = self.process.stderr.read()
        if self.process.returncode != 0:
            self.model.update_output("Fehlermeldung:\n" + stderr)
        print("... java program has terminated")

    @pyqtSlot()
    def stop(self):
        # Stop the Java program and terminate input/output monitoring.
        if self.process:
            self.process.kill()
        if self.output_monitor:
            self.output_monitor.stop()
        if self.input_monitor:
            self.input_monitor.stop()


class Output_Monitor(QThread):
    # Thread class to monitor and handle the output of a running Java program.
    data_signal = pyqtSignal(str)  # Signal to send data to the main thread

    def __init__(self, process, model):
        # Initialize the output monitor with the process and model.
        super(Output_Monitor, self).__init__()
        self.process = process
        self.model = model
        self.running = True

        # Connect signal to model update
        self.data_signal.connect(self.model.update_output)

    def run(self):
        # Monitor the output of the Java program and update the model.
        self.model.clear_output()
        total_output = ""
        while self.running:
            line = self.process.stdout.readline()  # Read one line at a time
            if line:  # Emit line immediately
                total_output += line
                self.data_signal.emit(total_output)
            elif self.process.poll() is not None:  # Stop if process is done
                break

        # Ensure remaining output is processed
        remaining_output = self.process.stdout.read()
        if remaining_output:
            self.data_signal.emit(remaining_output)

    def stop(self):
        # Stop monitoring the output.
        self.running = False



class Input_Monitor(QThread):
    # Thread class to monitor and handle the input for a running Java program.
    
    def __init__(self, process, model):
        # Initialize the input monitor with the process and model.
        super(Input_Monitor, self).__init__()
        self.process = process
        self.model = model
        self.running = True

    def run(self):
        # Monitor the input for the Java program and send it to the process.
        while self.running:
            if self.process.poll() is not None:
                self.running = False
                break
            if self.model.get_input_sent():
                self.model.set_input_sent(False)
                self.process.stdin.write(self.model.get_input() + "\n")
                self.process.stdin.flush()

    def stop(self):
        # Stop monitoring the input.
        self.running = False
        

def compile_java():
    # Compile the Java code and return the result of the compilation process.
    set_working_directory_java()
    print("starting compilation ...")
    try:
        p = subprocess.run(
            ["javac","Main.java"], 
            capture_output=True, 
            text=True, 
            check=True,
            creationflags=creation_flags)
        print("... compilation successful")
        error_code = "compilation successful"
    except subprocess.CalledProcessError as e: 
        print("... compilation failed")
        print("Error message: ", e.stderr)
        error_code = "Error message: " + e.stderr
    return(error_code)

def set_working_directory_java():
    # Change the working directory to the location of Java files.
    file_path = os.path.dirname(__file__)
    try:
        os.chdir(file_path + "/java_files")
    except:
        print("... there was an error setting the working directory")