from ir_step import IRStep

class SampleSizeStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        # working on it
        return "output"

    def n_accent(self, alpha, beta, p_0, p_1, delta, z):
        nominator = ()
        denominator = ()
        return float(nominator/denominator)**2

    def onfinish(self):
        print("finished step {}".format(self.name))