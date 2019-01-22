



class Click_Model(object):

    def __init__(self, gammas, data):
        self.gammas = gammas
        self.data = data


    def train(self):
        raise NotImplementedError("to be overrided")

    def apply(self, interleaving):
        raise NotImplementedError("to be overrided")

