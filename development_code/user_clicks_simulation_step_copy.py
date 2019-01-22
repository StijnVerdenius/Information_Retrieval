
#### DEVELOPPING ENVIRONMENT FOR ELIAS
###############################################################################################















import numpy as np
import copy
import random

f = open("data/YandexRelPredChallenge.txt", "r")
frame = []
for line in f:

    line = line.replace("\n", "")

    elements = line.split("	")

    if (elements[2] == "C"):
        dictionary = {"SessionID": int(elements[0]),
                      "TimePassed": int(elements[1]),
                      "TypeOfAction": elements[2],
                      "URLID": int(elements[3][:6])}
    elif (elements[2] == "Q"):
        dictionary = {"SessionID": int(elements[0]),
                      "TimePassed": int(elements[1]),
                      "TypeOfAction": elements[2],
                      "QueryID": int(elements[3]),
                      "RegionID": int(elements[4]),
                      "ListOfURLs": [int(x) for x in elements[5:]]

                      }
    else:
        raise Exception("contenttype not recognized, check load data function")

    frame.append(dictionary)


##############################################################################################################


def get_uq(data):
    """
    :param data - in the form of a list of libraries
    :return - library with key = document url, value = Query id: list of sessions
    """
    uq = {} #key = document url, value = Query id: list of sessions
    for i in frame:
        if i['TypeOfAction'] == 'Q':
            for u in i['ListOfURLs']:
                if u not in uq.keys():
                    uq[u] = {i['QueryID'] : [i['SessionID']]} # add url and corresponding query and session id
                if u in uq.keys():
                    if i['QueryID'] in uq[u].keys():          #check if document vs. query combo already exists
                        # if i['SessionID'] not in uq[u][i['QueryID']]: #check if session id already exists in document vs. query combo
                        uq[u][i['QueryID']].append(i['SessionID'])
                    else:
                        uq[u][i['QueryID']] = [i['SessionID']]
    return uq


def get_sc(data): # clicks for each session
    """
    :param data - in the form of a list of libraries
    :return - library where key = Session ID, value = query:[rank, url,click]
    """
    sc = {} #key = Session ID, value = (clicked rank, url)

    for i in frame:
        if i["SessionID"] not in sc.keys():
            sc[i['SessionID']] = {i['QueryID']:[]}

        if i['TypeOfAction'] == 'Q':
            if i['QueryID'] not in sc[i["SessionID"]].keys():
                sc[i['SessionID']][i['QueryID']] = [] #Empty if session does not result in click
            current_q = {"SessionID": i["SessionID"], "QueryID": i['QueryID'], "ListOfURLs": i["ListOfURLs"]}
            for r, u in enumerate(i["ListOfURLs"]):
                # print(sc[i['SessionID']][i['QueryID']])
                sc[i['SessionID']][i['QueryID']].append([r + 1, u, False])
        if i['TypeOfAction'] == 'C':
            for r,u in enumerate(current_q["ListOfURLs"]):
                if u == i["URLID"]:
                    for sublist in sc[i['SessionID']][current_q['QueryID']]:
                        if sublist[1] == u:
                            sublist[2] = True
    return sc


def init_alphas(data, value):
    """
    :param data -  in the form of a list of libraries
    :return - library where key = document, value = query : a_uq
    """
    alphas = {} # key = document, value = query : a_uq
    for f in frame:
        if f['TypeOfAction'] == 'Q':
            for u in f["ListOfURLs"]:
                if u not in alphas.keys():
                    alphas[u] = {f['QueryID']:value}
                if u in alphas.keys():
                    if f['QueryID'] not in alphas[u].keys():
                        alphas[u][f['QueryID']] = value
    return alphas



def alpha_update(alphas, gammas, uq, sc, data):
    """
    :param alphas - library where key = document, value = query : a_uq
    :param gammas - list of 10 gammas
    :param uq - library with key = document url, value = Query id: list of sessions
    :param sc - library where key = Session ID, value = (clicked rank, url)
    :return - update by iterating though all query vs. document seshs
    """
    # alpha2 = copy.deepcopy(alphas) #key = document u, value = query: a_uq
    alpha2 = init_alphas(data, 1)
    rank = 1 # init rank
    click = 0 #initialize click

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
                # print('document = ',document, ', query = ', query, ', session = ',session)
                # print('rank = ',rank)
                if (click == 0):
                    fraction = ((1 - gammas[rank-1])*alphas[document][query])/(1 - (gammas[rank-1]*alphas[document][query])) # check alphas[document][query]
                    alpha2[document][query] += fraction
                else:
                    alpha2[document][query] += 1
                # counter += 1
            # print('a be4 =', alpha2[document][query])
            alpha2[document][query] /= counter

            if alpha2[document][query] < 0:
                raise Exception

            if alpha2[document][query] > 1:
                raise Exception
    return alpha2


def gamma_update(alphas, gammas, uq, sc):
    """
    :param alphas - library where key = document, value = query : a_uq
    :param gammas - list of 10 gammas
    :param uq - library with key = document url, value = Query id: list of sessions
    :param sc - library where key = Session ID, value = (clicked rank, url)
    :return - list of updated gammas
    """
    s_r = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0} #sessions per rank (counter)
    # counter = 0
    gamma = np.zeros(len(gammas))
    rank = 1 # initialize rank
    click = 0 #initialize click
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
                    fraction = (gammas[rank-1]*(1-alphas[document][query]))/(1-gammas[rank-1]*alphas[document][query])
                    # print(fraction)

                    gamma[rank-1] += fraction
                else:
                    gamma[rank-1] += 1
                # print('rank = ',rank)
                # s_r[rank] += 1
                # counter += 1

    for g in range(len(gamma)):
        gamma[g] /= s_r[g+1]
    # gamma /= counter

    return list(np.around(gamma,4))



def EMtrain(data):
    uq = get_uq(data) #change frame to whatever is the data saved as
    sc = get_sc(data)
    alphas = init_alphas(data, 0.2) # initializing first alpha
    # gammas = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    gammas = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    gs = [gammas]
    als = [alphas]
    convergence_e = 0.01
    counter = 0

    while 1==1: #infinite loop
        current_g = gamma_update(als[counter], gs[counter], uq, sc)
        # current_g = gamma_update(alphas, gs[counter], uq, sc)
        gs.append(current_g)

        current_a = alpha_update(als[counter], gs[counter], uq, sc, data)
        als.append(current_a)

        counter += 1
        print('')
        print('iteration number = ', counter)
        print('gs = ', current_g)
        if np.linalg.norm(np.array(gs[counter]) - np.array(gs[counter-1])) < convergence_e and counter > 0: # Convergence criteria
            break
    return current_a, current_g
    # return current_g

a, g = EMtrain(frame)
# g = EMtrain(frame)


def apply_PBM(i_ranks, gammas):
    epsilon = 1e-6
    i_list = i_ranks.get_interleaved_ranking()

    for index, e in i_list:
        r = e.relevance_to_int()
        if r == 1:
            a = 1 - epsilon
        else:
            a = epsilon

        if random.random() <= gammas[element]*a:
            i_ranks.insertclick(index)


############################################################################################## ----- RCM



def RCMtrain(data):
    sc = get_sc(data)
    numerator = 0
    denominator = 0
    for session in sc:
        for query in sc[session]:
            for document in sc[session][query]:
                if document[2] is True:
                    numerator += 1
                denominator += 1

    rho = numerator/denominator

    return rho


rho = RCMtrain(frame)


def apply_RCM(i_ranks, rho):
    i_list = i_ranks.get_interleaved_ranking()

    for index, e in i_list:
        if random.random() <= rho:
            i_ranks.insertclick(index)
















#
# def apply_RCM(i_ranks):
#     p_click = i_list = i_ranks.get_interleaved_ranking()
#
