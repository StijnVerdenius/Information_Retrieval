
from ir_step import IRStep

class UserClicksSimulationStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        print("some stuff happening.. (dummy ouyput)")
        return "output"

    def onfinish(self):
        print("finished step {}".format(self.name))


###############################################################################################


f = open("data/YandexRelPredChallenge.txt", "r")
frame = []
for line in f:

    line = line.replace("\n", "")

    elements = line.split("	")

    if (elements[2] == "C"):
        dictionary = {"SessionID": int(elements[0]),
                      "TimePassed": int(elements[1]),
                      "TypeOfAction": elements[2],
                      "URLID": int(elements[3])}
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




# qs = {} #key = Query ID, value = list of libraries with key - Session ID, value - List of URLs
#
# for i in frame:
#     if i['TypeOfAction'] == 'Q':
#         current_s = {i['SessionID']:i['ListOfURLs']}
#         if i['QueryID'] not in qs.keys():
#             qs[i['QueryID']] = [current_s]
#         elif i['QueryID'] in qs.keys():
#             qs[i['QueryID']].append(current_s)
#
# print(qs.values())


# alphas = {} # key = document, value = query : a_uq
# for f in frame:
#     if f['TypeOfAction'] == 'Q':
#         for u in f["ListOfURLs"]:
#             if u not in alphas.keys():
#                 alphas[u] = {f['QueryID']:0.5}
#             if u in alphas.keys():
#                 if f['QueryID'] not in alphas[u].keys():
#                     alphas[u][f['QueryID']] = 0.5



uq = {} #key = document url, value = Query id: list of sessions
for i in frame:
    if i['TypeOfAction'] == 'Q':
        for u in i['ListOfURLs']:
            if u not in uq.keys():
                uq[u] = {i['QueryID'] : [i['SessionID']]} # add url and corresponding query and session id
            if u in uq.keys():
                if i['QueryID'] in uq[u].keys():          #check if document vs. query combo already exists
                    if i['SessionID'] not in uq[u][i['QueryID']]: #check if session id already exists in document vs. query combo
                        uq[u][i['QueryID']].append(i['SessionID'])
                else:
                    uq[u][i['QueryID']] = [i['SessionID']]

# print(uq[17560])





sc = {}
sc_id = {}
for i in frame:
    if i["SessionID"] not in sc.keys():
        sc[i['SessionID']] = [] #Empty if session does not result in click
        sc_id[i['SessionID']] = []
    if i['TypeOfAction'] == 'Q':
        current_q = {"SessionID": i["SessionID"], "ListOfURLs": i["ListOfURLs"][:6]}
    if i['TypeOfAction'] == 'C':
        for e in enumerate(current_q["ListOfURLs"]):
            if e[1] == i["URLID"]:
                rank = e[0]+1
                sc_id[i['SessionID']].append(i["URLID"])
        sc[i['SessionID']].append(rank) #The rank of the url id clicked in the given session

print(sc[0])
print(sc_id[0])



# for document in uq:
#     for query in uq[document]:
#         for session in uq[document][query]:
#             # print(session)
#             if session in sc_id.keys():
#                 if document in sc_id[session]:
#                     click = 1
#                 else:
#                     click = 0


#
#
# sc = {} #key = Session ID, value = clicked rank
#
# for i in frame:
#     if i["SessionID"] not in sc.keys():
#         sc[i['SessionID']] = [] #Empty if session does not result in click
#
#     if i['TypeOfAction'] == 'Q':
#         current_q = {"SessionID": i["SessionID"], "ListOfURLs": i["ListOfURLs"][:6]}
#
#     if i['TypeOfAction'] == 'C':
#
#         for e in enumerate(current_q["ListOfURLs"]):
#             if e[1] == i["URLID"]:
#                 rank = e[0]+1
#
#         sc[i['SessionID']].append(rank) #The rank of the url id clicked in the given session


# print(len(list(sc.keys())),'sc should be 11717')

###############################################################################################

# def get_sessions_per_query(data):
#     """
#     :param data - in the form of a list of libraries
#     :return - library where key = Query ID, value = (Session IDs, list of URLs)
#     """
#     qs = {}
#     for i in frame:
#         if i['TypeOfAction'] == 'Q':
#             if i['QueryID'] not in qs.keys():
#                 qs[i['QueryID']] = ([i['SessionID']], i['ListOfURLs'])
#             elif i['QueryID'] in qs.keys():
#                 qs[i['QueryID']][0].append(i['SessionID'])
#     return qs


def get_uq(data):
    """
    :param data - in the form of a list of libraries
    :return - library with key = document url, value = Query id: list of sessions
    """
    uq = {}
    for i in frame:
        if i['TypeOfAction'] == 'Q':
            for u in i['ListOfURLs']:
                if u not in uq.keys():
                    uq[u] = {i['QueryID'] : [i['SessionID']]} # add url and corresponding query and session id
                if u in uq.keys():
                    if i['QueryID'] in uq[u].keys():          #check if document vs. query combo already exists
                        if i['SessionID'] not in uq[u][i['QueryID']]: #check if session id already exists in document vs. query combo
                            uq[u][i['QueryID']].append(i['SessionID'])
                    else:
                        uq[u][i['QueryID']] = [i['SessionID']]

    return uq




def get_sc(data):
    """
    :param data - in the form of a list of libraries
    :return - library where key = Session ID, value = clicked rank
            & library where key = Session ID, value = clicked id
    """
    sc = {}
    sc_id = {}
    for i in data:
        if i["SessionID"] not in sc.keys():
            sc[i['SessionID']] = [] #Empty if session does not result in click
            sc_id[i['SessionID']] = []
        if i['TypeOfAction'] == 'Q':
            current_q = {"SessionID": i["SessionID"], "ListOfURLs": i["ListOfURLs"][:6]} # may need to remove :6!!!!!!!!!
        if i['TypeOfAction'] == 'C':
            for e in enumerate(current_q["ListOfURLs"]):
                if e[1] == i["URLID"]:
                    rank = e[0]+1
                    sc_id[i['SessionID']].append(i["URLID"])
            sc[i['SessionID']].append(rank) #The rank of the url id clicked in the given session
    return sc, sc_id




def init_alphas(data):
    """
    :param data -  in the form of a list of libraries
    :return - library where key = document, value = query : a_uq
    """
    alphas = {} # key = document, value = query : a_uq
    for f in frame:
        if f['TypeOfAction'] == 'Q':
            for u in f["ListOfURLs"]:
                if u not in alphas.keys():
                    alphas[u] = {f['QueryID']:0.5}
                if u in alphas.keys():
                    if f['QueryID'] not in alphas[u].keys():
                        alphas[u][f['QueryID']] = 0.5
    return alphas




def alpha_update(alphas, gammas, uq, sc_id, sc):
    """
    :return - update by iterating though all query vs. document seshs
    """
    for document in uq:
        for query in uq[document]:
            counter = 0
            for session in uq[document][query]:
                counter += 1
                if session in sc_id.keys():
                    if document in sc_id[session]: #gives click for session of u vs. q combo
                        click = 1
                    else:
                        click = 0

                for i,d in enumerate(sc_id[session]): # get corresponding rank of document clicked
                    if d == document:
                        rank = sc[session][i]

                fraction = ((1 - gammas[rank])*alphas[document][query])/(1 - (gammas[rank]*alphas[document][query])) # check alphas[document][query]

                alphas[document][query] += (click + (1-click)*(fraction))
            alphas[document][query] /= counter
    return alphas




def gamma_update(alphas, gammas):
    for r in







# def EMiter(data):
#     uq = get_uq(data) #change frame to whatever is the data saved as
#     sc, sc_id = get_sc(data)
#     alphas = init_alphas(data) # initializing first alpha
#     gammas = [1, 0.8, 0.6, 0.4, 0.2, 0.0] #initializing gammas



#
# def EMtrain(data):
#
#


