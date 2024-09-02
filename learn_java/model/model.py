from model.handling import Handling
from model.chains import Chains
from model.tutorial import Tutorial_Handling

class Model(Handling, Tutorial_Handling, Chains):
    # main model
    def __init__(self):
        super(Model,self).__init__()