
from ir_step import IRStep

class ERRStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):

        ranking_pairs = input_list[0]

        print("some stuff happening.. (dummy ouyput)")

        ERR_TABLE = None # TODO
        length_of_each_ranking = None #TODO

        # todo: agree on input-output (see step 3)



        return ERR_TABLE, length_of_each_ranking

    def onfinish(self):
        print("finished step {}".format(self.name))