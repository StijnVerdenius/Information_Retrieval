from models.interleavings.interleaving import Interleaving
from random import choice, randint
from copy import deepcopy

from models.document import Document
from models.relevance import Relevance


class TeamDraftInterleaving(Interleaving):

    def __init__(self, ranking1, ranking2, cutoff=None):
        super().__init__(ranking1, ranking2, cutoff)

    def interleave_docs(self):
        counters = [len(self.ranking1), len(self.ranking2)]
        rankings = deepcopy([self.ranking1, self.ranking2])

        while(sum(counters) > 0 ):

            # flip coin
            which_first = choice([1, 0])
            which_second = int(not which_first)

            # take doc from chosen ranking, skip if it is empty
            if (counters[which_first] == 0):
                continue
            counters[which_first] -= 1
            picked_document = rankings[which_first].pop(0)

            # get doc ids from the other ranking and see at what places the doc occurs
            doc_ids_second_player = [doc.id for doc in rankings[which_second]]
            indices = [i for i, x in enumerate(doc_ids_second_player) if x == picked_document.id]

            # remove at those places
            for ind in indices:
                removed = rankings[which_second].pop(ind)
                counters[which_second] -= 1

                # make sure the removed objects ar identical
                assert removed.id == picked_document.id, "Mistake in teamdraft: removing docs from other ranking"

            # insert into interleaving
            self.position2ranking[len(self.interleaved)] = "ranking"+str(which_first+1)
            self.interleaved.append(picked_document)

        # make sure both rankings are empty
        assert len(rankings[0]) + len(rankings[1]) == 0, "Mistake: not ranking all"



