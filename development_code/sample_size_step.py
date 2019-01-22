from ir_step import IRStep

import math

import numpy as np

class SampleSizeStep(IRStep):

    def __init__(self, name, purpose, data):
        self.k = 100
        self.alpha = 0.05
        self.beta = 0.1
        self.p_0 = 0.5
        super().__init__(name, purpose, data)


    def onStart(self, input_list):

        total_table = {}

        for click_model in input_list:

            total_table[click_model] = {}

            for interleaving_type in input_list[click_model]:

                total_table[click_model][interleaving_type] = {}

                for bin in input_list[click_model][interleaving_type]:

                    bin = str(bin)

                    total_table[click_model][interleaving_type][bin] = []

                    for percentage in input_list[click_model][interleaving_type][int(bin)]:

                        total_table[click_model][interleaving_type][bin].append(self.n(self.alpha, self.beta, self.p_0, percentage))


                    max = "None"
                    min = "None"
                    median = "None"
                    mean = "None"

                    if (len(total_table[click_model][interleaving_type][bin]) > 0):

                        max = np.max(total_table[click_model][interleaving_type][bin])
                        min = np.min(total_table[click_model][interleaving_type][bin])
                        median = np.median(total_table[click_model][interleaving_type][bin])
                        mean = np.mean(total_table[click_model][interleaving_type][bin])

                    total_table[click_model][interleaving_type][bin] = { "max" : max, "min" : min, "median": median, "mean" : mean} #,"list" : total_table[click_model][interleaving_type]}

        return total_table

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



    def onfinish(self):
        print("finished step {}".format(self.name))