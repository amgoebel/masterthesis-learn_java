from model.handling import Handling
from model.chains import Chains

class Model(Handling, Chains):
    # Main model class that combines handling and chains for managing data and interactions.
    def __init__(self):
        super(Model,self).__init__()