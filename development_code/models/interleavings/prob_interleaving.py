
from models.interleavings.interleaving import Interleaving
from copy import deepcopy
from random import choice

import itertools

from models.document import Document
from models.relevance import Relevance

import numpy as np


class ProbabilisticInterleaving(Interleaving):

    def __init__(self, ranking1, ranking2, distribution, cutoff=None):
        self.distribution = distribution
        assert len(distribution) == len(ranking1) == len(
            ranking2), "rankings and/or distribution not fo the same lengths"
        self.possible_generators = len(ranking1) * len(ranking2)
        self.position2chance = {}
        super().__init__(ranking1, ranking2, cutoff)


    def interleave_docs(self):
        counters = [len(self.ranking1), len(self.ranking2)]
        rankings = deepcopy([self.ranking1, self.ranking2])
        distributions = deepcopy([self.distribution])+deepcopy([self.distribution])

        while (sum(counters) > 0):

            # flip coin
            which_first = choice([1, 0])
            which_second = int(not which_first)

            # take doc from chosen ranking, skip if it is empty
            if (counters[which_first] == 0):
                continue
            counters[which_first] -= 1
            picked_index = np.random.choice(range(len(distributions[which_first])), p=self.softmax(distributions[which_first]), replace=False)
            picked_document = rankings[which_first].pop(picked_index)
            chance_which_first = distributions[which_first].pop(picked_index)

            # get doc ids from the other ranking and see at what places the doc occurs
            doc_ids_second_player = [doc.id for doc in rankings[which_second]]
            indices = [i for i, x in enumerate(doc_ids_second_player) if x == picked_document.id]

            chance_which_second = 0
            # remove at those places
            for ind in indices:

                removed = rankings[which_second].pop(ind)
                chance_which_second = None
                counters[which_second] -= 1

                # make sure the removed objects ar identical
                assert removed.id == picked_document.id, "Mistake in prob-interleaving: removing docs from other ranking"

            # insert into interleaving
            self.position2chance[len(self.interleaved)] = {which_first: chance_which_first, which_second: chance_which_second}
            self.interleaved.append(picked_document)

        # make sure both rankings are empty
        assert len(rankings[0]) + len(rankings[1]) == 0, "Mistake: not ranking all"

        # get all permutations that coudve generated this interleaving
        chance_of_permutations = []
        contribution_permutations = list(itertools.product([0, 1], repeat=len(self.interleaved)))

        # get the prior chance of that permutation
        for permutation in contribution_permutations:
            chance_of_permutations.append(float(sum([self.position2chance[i][r] for i, r in zip(range(len(self.interleaved)), permutation)])/self.possible_generators))

        # for both rankings, calculate expectated clicks earned for each click on each position
        for position in range(len(self.interleaved)):

            expectations = [0,0]

            for chance, permutation in zip(chance_of_permutations, contribution_permutations):
                expectations[permutation[position]] += self.position2chance[position][permutation[position]]*chance

            self.position2ranking[position] = {0: expectations[0], 1 : expectations[1]}



    def insertclick(self, position):
        self.score["ranking1"] += self.position2ranking[position][0]
        self.score["ranking2"] += self.position2ranking[position][1]


    def softmax(self, distribution):
        summation = sum(distribution)
        return [float(x/summation) for x in distribution]

    def pop_distribution(self, index, distributions, which_second):
        return distributions[which_second].pop(index)




draft = ProbabilisticInterleaving([Document(x, Relevance(Relevance.NOT_RELEVANT)) for x in range(2)], [Document(x, Relevance(Relevance.NOT_RELEVANT)) for x in range(2)][::-1], [0.6, 0.4])

print(len(draft.interleaved))
print([x.id for x in draft.interleaved])
print(draft.position2ranking)

print(draft.score)
draft.insertclick(0)
draft.insertclick(1)
# draft.insertclick(2)

print(draft.score)
print(draft.get_winner())