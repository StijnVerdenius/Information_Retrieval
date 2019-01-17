
from step_general import Step

class Step1(Step):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        print("some stuff happening.. (dummy ouyput)")
        return "output"

    def onfinish(self):
        print("\n\nfinished step {}\n\n".format(self.name))