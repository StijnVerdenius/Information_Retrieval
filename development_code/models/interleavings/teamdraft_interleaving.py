from models.interleavings.interleaving import Interleaving
from random import choice, randint
from copy import deepcopy


class TeamDraftInterleaving(Interleaving):

    def __init__(self, alg_P, alg_E, cutoff=None):
        super().__init__(alg_P, alg_E, cutoff)

    def _interleave_docs(self): # PRIVATE
        """ implementation of interleaving """

        counters = [len(self.alg_P), len(self.alg_E)]
        rankings = deepcopy([self.alg_P, self.alg_E])

        while(sum(counters) > 0):

            # flip coin
            which_first = choice([1, 0])
            which_second = int(not which_first)

            # take doc from chosen ranking, skip if it is empty
            if (counters[which_first] == 0):
                continue
            counters[which_first] -= 1
            picked_document = rankings[which_first].pop(0)

            self._remove_duplicates_from_other_ranking(rankings, picked_document, counters, which_second)

            # insert into interleaving
            self.position2ranking[len(self.interleaved)] = which_first
            self.interleaved.append(picked_document)

        # make sure both rankings are empty
        assert len(rankings[0]) + len(rankings[1]) == 0, "Mistake: not ranking all docs"
