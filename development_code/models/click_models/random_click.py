

from models.click_models.click_model import Click_Model
import random

class Random_Click_Model(Click_Model):

    def __init__(self, gammas, data):
        super().__init__(gammas, data)


    def train(self):
        print("Starting training")

        # ELIAS ADD TRAINING CODE HERE
        raise NotImplementedError("ELIAS ADD TRAINING CODE HERE")


    def apply(self, interleaving):
        #same as pbm or not?
        raise NotImplementedError("ELIAS ADD APPLY CODE HERE")
