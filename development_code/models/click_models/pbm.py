

from models.click_models.click_model import Click_Model
import random

import numpy as np

class PBM(Click_Model):

    def __init__(self, parameters, data):
        super().__init__(parameters, data)


    def train(self):
        print("Starting training")

        uq = self.get_uq()  # change frame to whatever is the data saved as
        sc = self.get_sc()
        alphas = self.init_alphas(0.2)  # initializing first alpha
        # gammas = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        gammas = self.parameters
        gs = [gammas]
        als = [alphas]
        convergence_e = 0.01
        counter = 0

        while 1 == 1:  # infinite loop
            current_g = self.gamma_update(als[-1], gs[-1], uq, sc)
            # current_g = gamma_update(alphas, gs[counter], uq, sc)
            gs.append(current_g)

            current_a = self.alpha_update(als[-1], gs[-1], uq, sc)
            als.append(current_a)

            if (len(als) > 3):
                als.pop(0)

            if (len(gs) > 3):
                gs.pop(0)

            counter += 1
            print('\riteration number = {} gs = {}'.format(counter, current_g), end='')
            if np.linalg.norm(np.array(gs[-1]) - np.array(gs[-2])) < convergence_e and counter > 0:  # Convergence criteria
                print("\n")
                self.parameters = current_g
                return

    def apply(self, interleaving):


        interleaving.reset_score()

        epsilon = 1e-6
        interleaving_list = interleaving.get_interleaved_ranking()

        for index, document in enumerate(interleaving_list):
            relevance = document.relevance_to_int()
            if relevance == 1:
                alpha = 1 - epsilon
            else:
                alpha = epsilon

            dice = random.random()

            evaluated = self.parameters[index] * alpha

            if dice <= evaluated:
                interleaving.insertclick(index)

    def get_uq(self):
        """
        :param data - in the form of a list of libraries
        :return - library with key = document url, value = Query id: list of sessions
        """
        uq = {}  # key = document url, value = Query id: list of sessions
        for i in self.data:
            if i['TypeOfAction'] == 'Q':
                for u in i['ListOfURLs']:
                    if u not in uq.keys():
                        uq[u] = {i['QueryID']: [i['SessionID']]}  # add url and corresponding query and session id
                    if u in uq.keys():
                        if i['QueryID'] in uq[u].keys():  # check if document vs. query combo already exists
                            uq[u][i['QueryID']].append(i['SessionID'])
                        else:
                            uq[u][i['QueryID']] = [i['SessionID']]
        return uq



    def init_alphas(self, value):
        """
        :param data -  in the form of a list of libraries
        :return - library where key = document, value = query : a_uq
        """
        alphas = {}  # key = document, value = query : a_uq
        for f in self.data:
            if f['TypeOfAction'] == 'Q':
                for u in f["ListOfURLs"]:
                    if u not in alphas.keys():
                        alphas[u] = {f['QueryID']: value}
                    if u in alphas.keys():
                        if f['QueryID'] not in alphas[u].keys():
                            alphas[u][f['QueryID']] = value
        return alphas

    def alpha_update(self, alphas, gammas, uq, sc):
        """
        :param alphas - library where key = document, value = query : a_uq
        :param gammas - list of 10 parameters
        :param uq - library with key = document url, value = Query id: list of sessions
        :param sc - library where key = Session ID, value = (clicked rank, url)
        :return - update by iterating though all query vs. document seshs
        """
        alpha2 = self.init_alphas(1)
        rank = 1  # init rank
        click = 0  # initialize click

        for document in uq:
            for query in uq[document]:
                counter = 2

                for session in uq[document][query]:
                    counter += 1
                    for e in sc[session][query]:
                        if document == e[1]:
                            rank = e[0]
                            if e[2] == True:
                                click = 1
                            else:
                                click = 0
                            break

                    if (click == 0):
                        fraction = ((1 - gammas[rank - 1]) * alphas[document][query]) / (
                                    1 - (gammas[rank - 1] * alphas[document][query]))  # check alphas[document][query]
                        alpha2[document][query] += fraction
                    else:
                        alpha2[document][query] += 1

                alpha2[document][query] /= counter

                if alpha2[document][query] < 0:
                    raise Exception

                if alpha2[document][query] > 1:
                    raise Exception
        return alpha2

    def gamma_update(self, alphas, gammas, uq, sc):
        """
        :param alphas - library where key = document, value = query : a_uq
        :param gammas - list of 10 parameters
        :param uq - library with key = document url, value = Query id: list of sessions
        :param sc - library where key = Session ID, value = (clicked rank, url)
        :return - list of updated parameters
        """
        s_r = {key+1 : 0 for key in range(len(gammas))}#, 7: 0, 8: 0, 9: 0, 10: 0}  # sessions per rank (counter)
        # counter = 0
        gamma = np.zeros(len(gammas))
        rank = 1  # initialize rank
        click = 0  # initialize click
        for document in uq:
            for query in uq[document]:
                for session in uq[document][query]:
                    for e in sc[session][query]:
                        if document == e[1]:
                            rank = e[0]
                            s_r[rank] += 1
                            if e[2] == True:
                                click = 1
                            else:
                                click = 0
                            break

                    if (click == 0):
                        fraction = (gammas[rank - 1] * (1 - alphas[document][query])) / (
                                    1 - gammas[rank - 1] * alphas[document][query])

                        gamma[rank - 1] += fraction
                    else:
                        gamma[rank - 1] += 1


        for g in range(len(gamma)):
            gamma[g] /= s_r[g + 1]

        return list(np.around(gamma, 4))


