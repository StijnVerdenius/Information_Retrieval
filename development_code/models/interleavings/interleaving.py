
import numpy as np
from typing import List
from models.document import Document

"""
Main interleaving class, parent to specific interleavings

Holds some main functionality
"""

class Interleaving(object):


    def __init__(self, alg_P, alg_E, cutoff=None):
        self.alg_P = alg_P
        self.alg_E = alg_E
        self.ranking2algorithm = {0: "P", 1: "E"}
        self.position2ranking = {}
        self.interleaved = []
        self.score = {"E" : 0, "P" : 0}
        self._interleave_docs()
        if (not cutoff == None):
            self.cut_off_at(cutoff)
        self.registered_clicks = 0
        self.click_history = []

    def _interleave_docs(self): #PRIVATE
        """ method contracty to be overrided by child-classes """

        raise NotImplementedError("To be overrided by child class")

    def insertclick(self, position):  # USE THIS ONE
        """ stores a click in the interleaving such that later the score can be extracted """

        self.score[self.ranking2algorithm[self.position2ranking[position]]] += 1
        self.registered_clicks += 1
        self.click_history.append(position)

    def get_interleaved_ranking(self) -> List[Document]: # USE THIS ONE
        """ returns list of documents """

        return self.interleaved

    def get_click_history(self): # USE THIS ONE
        return self.click_history

    def get_score(self): # USE THIS ONE
        """ returns the score of the two isnerted rankings given currently registered clicks """

        return self.score

    def reset_score(self): ## USE THIS ONE
        """ resets counters but leaves interleaving intact """

        self.score = {"E": 0, "P": 0}
        self.registered_clicks = 0
        self.click_history = []

    def get_winner(self): # USE THIS ONE
        """ gets winner of interleaving """

        if (self.score["E"] == self.score["P"]):
            return -1
        return max(self.score, key=self.score.get)

    def cut_off_at(self, cutoff): # USE THIS ONE (IF NEEDED)
        """ cuts off interleaving after certain rank. note: expectations are not recalculated """

        self.interleaved = self.interleaved[:cutoff]
        for key in list(self.position2ranking):
            if (key > cutoff):
                del self.position2ranking[key]

    def _remove_duplicates_from_other_ranking(self, rankings, picked_document, counters, which_second, distributions=None): #PRIVATE
        """ buisiness logic function for removing duplicates out of the ranking whos turn it is not to add a element to the interleaving """

        # get doc ids from the other ranking and see at what places the doc occurs
        doc_ids_second_player = [doc.id for doc in rankings[which_second]]

        if (picked_document.id in doc_ids_second_player):
            index = doc_ids_second_player.index( picked_document.id)

            removed = rankings[which_second].pop(index)
            counters[which_second] -= 1

            # make sure the removed objects ar identical
            assert removed.id == picked_document.id, "Mistake in prob-interleaving: removing docs from other ranking"

            return self._pop_distribution(index, distributions, which_second)
        else:
            return 0

    def _pop_distribution(self, index, distributions, which_second): #PRIVATE
        """ to be overrided by child-classes that utilize it, to be ignored by those who don't """

        pass

    def __str__(self): #TO STRING
        return "Interleaving: " + str(self.get_interleaved_ranking()) + ", Scores: " + str(self.score), ", Registered clicks: "+ str(self.registered_clicks)