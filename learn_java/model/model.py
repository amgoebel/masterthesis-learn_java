from model.java_handling import Java_Handling
from model.chains import Chains

class Model(Java_Handling, Chains):
    def __init__(self):
        super(Model,self).__init__()