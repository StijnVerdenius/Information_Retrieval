

from models.click_models.click_model import Click_Model
import random

class PBM(Click_Model):

    def __init__(self, gammas, data):
        super().__init__(gammas, data)


    def train(self):
        # ELIAS ADD TRAINING CODE HERE
        raise NotImplementedError("ELIAS ADD TRAINING CODE HERE")

    def apply(self, interleaving):
        epsilon = 1e-6
        interleaving_list = interleaving.get_interleaved_ranking()

        for index, document in interleaving_list:
            relevance = document.relevance_to_int()
            if relevance == 1:
                alpha = 1 - epsilon
            else:
                alpha = epsilon

            if random.random() <= self.gammas[index] * alpha:
                interleaving.insertclick(index)
