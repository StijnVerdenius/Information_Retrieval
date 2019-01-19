
import numpy as np

class Interleaving(object):

    def __init__(self, ranking1, ranking2, cutoff=None):
        self.ranking1 = ranking1
        self.ranking2 = ranking2
        self.position2ranking = {}
        self.interleaved = []
        self.score = {"ranking1" : 0, "ranking2" : 0}
        self.interleave_docs()
        if (not cutoff == None):
            self.cut_off_at(cutoff)

    def interleave_docs(self):
        raise NotImplementedError("To be overrided by child class")

    def insertclick(self, position):
        self.score[self.position2ranking[position]] += 1

    def get_interleaved_ranking(self):
        return self.interleaved

    def get_score(self):
        return self.score

    def get_winner(self):
        scores = self.score[["ranking" + str(i) for i in range(len(self.score))]]
        return np.argmax(scores)+1

    def cut_off_at(self, cutoff):
        self.interleaved = self.interleaved[:cutoff]
        for key in self.position2ranking:
            if (key > cutoff):
                del self.position2ranking[key]