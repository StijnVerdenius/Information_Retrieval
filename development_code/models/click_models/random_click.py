

from models.click_models.click_model import Click_Model
import random

class Random_Click_Model(Click_Model):

    def __init__(self, parameters, data):
        super().__init__(parameters, data)


    def train(self):
        print("Starting training")

        sc = self.get_sc()
        numerator = 0
        denominator = 0
        for session in sc:
            for query in sc[session]:
                for document in sc[session][query]:
                    if document[2] is True:
                        numerator += 1
                    denominator += 1

        rho = numerator / denominator

        self.parameters = rho
        print("Final rho {}".format(rho))
        return


    def apply(self, interleaving):
        interleaving.reset_score()

        interleaving_list = interleaving.get_interleaved_ranking()

        for index, _ in enumerate(interleaving_list):
            if random.random() <= self.parameters:
                interleaving.insertclick(index)
