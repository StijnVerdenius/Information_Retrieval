from models.interleavings.interleaving import Interleaving
from random import choice, randint
from copy import deepcopy


class TeamDraftInterleaving(Interleaving):

    def __init__(self, ranking1, ranking2, cutoff=None):
        super().__init__(ranking1, ranking2, cutoff)

    def _interleave_docs(self): # PRIVATE
        """ implementation of interleaving """

        counters = [len(self.ranking1), len(self.ranking2)]
        rankings = deepcopy([self.ranking1, self.ranking2])

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
            self.position2ranking[len(self.interleaved)] = "ranking"+str(which_first+1)
            self.interleaved.append(picked_document)

        # make sure both rankings are empty
        assert len(rankings[0]) + len(rankings[1]) == 0, "Mistake: not ranking all docs"
