
from models.interleavings.interleaving import Interleaving
from copy import deepcopy
from random import choice
import itertools
import numpy as np
from utils import softmax


class ProbabilisticInterleaving(Interleaving):

    def __init__(self, ranking1, ranking2, distribution, cutoff=None):
        self.distribution = distribution
        assert len(distribution) == len(ranking1) == len(
            ranking2), "rankings and/or distribution not fo the same lengths"
        self.possible_generators = len(ranking1) * len(ranking2)
        self.position2chance = {}
        super().__init__(ranking1, ranking2, cutoff)


    def interleave_docs(self):
        """ implementation of interleaving """

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
            picked_index = np.random.choice(range(len(distributions[which_first])), p=softmax(distributions[which_first]), replace=False)
            picked_document = rankings[which_first].pop(picked_index)
            chance_which_first = self.pop_distribution(picked_index, distributions, which_first)

            # remove from other ranking
            chance_which_second = self.remove_duplicates_from_other_ranking(rankings, picked_document, counters, which_second, distributions=distributions)

            # insert into interleaving
            self.position2chance[len(self.interleaved)] = {which_first: chance_which_first, which_second: chance_which_second}
            self.interleaved.append(picked_document)

        # make sure both rankings are empty
        assert len(rankings[0]) + len(rankings[1]) == 0, "Mistake: not ranking all docs"

        # complete expectation calculation
        self.fill_in_expectations()



    def insertclick(self, position):
        """ implementation of click-saving """

        self.score["ranking1"] += self.position2ranking[position][0]
        self.score["ranking2"] += self.position2ranking[position][1]

        self.registered_clicks += 1

    def pop_distribution(self, index, distributions, which):
        """ removes element form probability distribution as to be consistent with the documents to be interleaved"""

        return distributions[which].pop(index)

    def fill_in_expectations(self):
        """ pre-calculates the expectation that is added to both players per new future click """

        # get all permutations that could've generated this interleaving
        chance_of_permutations = []
        contribution_permutations = list(itertools.product([0, 1], repeat=len(self.interleaved)))

        # get the prior chance of that permutation
        for permutation in contribution_permutations:
            chance_of_permutations.append(float(sum([self.position2chance[i][r] for i, r in zip(range(len(self.interleaved)), permutation)])/self.possible_generators))

        # for both rankings, calculate expectated clicks earned for each future click on each position
        for position in range(len(self.interleaved)):

            expectations = [0,0]

            for chance, permutation in zip(chance_of_permutations, contribution_permutations):
                expectations[permutation[position]] += self.position2chance[position][permutation[position]]*chance

            self.position2ranking[position] = {0: expectations[0], 1 : expectations[1]}