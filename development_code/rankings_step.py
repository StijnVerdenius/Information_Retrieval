from ir_step import IRStep

class RankingsStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)

    def onStart(self, input_list):
        print("some stuff happening.. (dummy output)")
        return "output"

    def onfinish(self):
        print("\n\nfinished step {}\n\n".format(self.name))