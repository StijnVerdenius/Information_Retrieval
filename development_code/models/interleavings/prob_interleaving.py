
from models.interleavings.interleaving import Interleaving

class ProbabilisticInterleaving(Interleaving):

    def __init__(self, ranking1, ranking2, distribution):
        super().__init__(ranking1, ranking2)
        self.distribution = distribution
        self.possible_generators = len(ranking1)*len(ranking2)

    def interleave_docs(self):
        pass

    def insertclick(self, position):
        pass