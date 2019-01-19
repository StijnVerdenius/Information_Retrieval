
import numpy as np
from typing import List
from models.document import Document

"""
Main interleaving class, parent to specific interleavings

Holds some main functionality
"""

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
        """ method contracty to be overrided by child-classes """

        raise NotImplementedError("To be overrided by child class")

    def insertclick(self, position):
        """ stores a click in the interleaving such that later the score can be extracted """

        self.score[self.position2ranking[position]] += 1

    def get_interleaved_ranking(self) -> List[Document]:
        """ returns list of documents """

        return self.interleaved

    def get_score(self):
        """ returns the score of the two isnerted rankings given currently registered clicks """

        return self.score

    def get_winner(self):
        """ """

        scores = [self.score["ranking" + str(i+1)] for i in range(len(self.score))]
        if (scores[0] == scores[1]):
            print("warning: tie in interleaving. '-1' returned")
            return -1
        return np.argmax(scores)+1

    def cut_off_at(self, cutoff):
        """ cuts off interleaving after certain rank. note: expectations are not recalculated """

        self.interleaved = self.interleaved[:cutoff]
        for key in self.position2ranking:
            if (key > cutoff):
                del self.position2ranking[key]

    def remove_duplicates_from_other_ranking(self, rankings, picked_document, counters, which_second, distributions=None):
        """ buisiness logic function for removing duplicates out of the ranking whos turn it is not to add a element to the interleaving """

        # get doc ids from the other ranking and see at what places the doc occurs
        doc_ids_second_player = [doc.id for doc in rankings[which_second]]
        index = doc_ids_second_player.index( picked_document.id)

        removed = rankings[which_second].pop(index)
        counters[which_second] -= 1

        # make sure the removed objects ar identical
        assert removed.id == picked_document.id, "Mistake in prob-interleaving: removing docs from other ranking"

        return self.pop_distribution(index, distributions, which_second)

    def pop_distribution(self, index, distributions, which_second):
        """ to be overrided by child-classes that utilize it, to be ignored by those who don't """

        pass