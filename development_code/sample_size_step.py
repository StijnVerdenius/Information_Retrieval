from ir_step import IRStep

import math

import numpy as np
import scipy.stats
from functools import lru_cache

class SampleSizeStep(IRStep):

    def __init__(self, name, purpose, data):
        self.alpha = 0.05
        self.beta = 0.1
        self.p_0 = 0.5
        super().__init__(name, purpose, data)


    def onStart(self, input_list):

        total_table = {}

        for cm_index, click_model in enumerate(input_list):

            total_table[click_model] = {}

            for it_index, interleaving_type in enumerate(input_list[click_model]):
                current_index = (cm_index + 1) + (it_index + 1)
                print(f'\rCalculating: {current_index}/4', end='')

                total_table[click_model][interleaving_type] = {}

                for bin in input_list[click_model][interleaving_type]:

                    str_bin = str(bin)

                    total_table[click_model][interleaving_type][str_bin] = []
                    current_bin = []

                    for percentage in input_list[click_model][interleaving_type][bin]:

                        # proportion_test =  self.n(self.alpha, self.beta, self.p_0, percentage)
                        proportion_test = self.proportion_test(percentage, self.alpha, self.beta, self.p_0)
                        if not proportion_test:
                            continue

                        # total_table[click_model][interleaving_type][bin].append(proportion_test)
                        current_bin.append(proportion_test)


                    max = "None"
                    min = "None"
                    median = "None"
                    mean = "None"
                    std = "None"

                    if (len(current_bin) > 0):

                        max = np.max(current_bin)
                        min = np.min(current_bin)
                        median = np.median(current_bin)
                        mean = np.mean(current_bin)
                        std = np.std(current_bin)

                    total_table[click_model][interleaving_type][str_bin] = { 
                        "max" : max, 
                        "min" : min, 
                        "median": median, 
                        "mean" : mean, 
                        "std": std
                    ,"list" : total_table[click_model][interleaving_type][str_bin]}

        print('\rCalculating: Done!')
        return total_table

    @lru_cache(maxsize=320000)
    def n(self, alpha, beta, p_0, p_1):

        z = (p_1-p_0)/(math.sqrt((p_0*(1-p_0)/self.k)))

        nominator = (
                    (z-alpha*math.sqrt(p_0*(1-p_0)))
                     +
                     (z-beta*math.sqrt(p_1*(1-p_1)))
                    )

        denominator = abs(p_1-p_0)

        if (denominator == 0):
            # instead of inf for printing reasons
            return 9999999999999999

        return round(float(nominator/denominator)**2 + float(1/denominator))

    @lru_cache(maxsize=320000)
    def proportion_test(self, p1, alpha = 0.5, beta = 0.1, p0 = 0.5):
        z_alpha = scipy.stats.norm.ppf(1-alpha)
        z_beta = scipy.stats.norm.ppf(1-beta)
        if p1 == p0:
            return None

        diff = p1 - p0
        # diff = 0.0001 if p1==p0 else p1-p0
        sample_size = p0 * (1 - p0) * (z_alpha + z_beta * np.sqrt((p1 * (1-p1))/(p0 *(1-p0)))/(diff))**2
        if sample_size==math.inf:
            print('INF:', p0, p1, z_alpha, z_beta)

        return sample_size

    def onfinish(self):
        print("finished step {}".format(self.name))