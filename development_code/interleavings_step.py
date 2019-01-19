
from ir_step import IRStep

class InterleavingsStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):




        return "output"

    def onfinish(self):
        print("finished step {}".format(self.name))