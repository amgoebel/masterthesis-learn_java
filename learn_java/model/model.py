from model.handling import Handling
from model.chains import Chains

class Model(Handling, Chains):
    # main model
    def __init__(self):
        super(Model,self).__init__()