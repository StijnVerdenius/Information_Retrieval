
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




qs = {} #key = Query ID, value = list of libraries with key - Session ID, value - List of URLs

for i in frame:
    if i['TypeOfAction'] == 'Q':
        current_s = {i['SessionID']:i['ListOfURLs']}
        if i['QueryID'] not in qs.keys():
            qs[i['QueryID']] = [current_s]
        elif i['QueryID'] in qs.keys():
            qs[i['QueryID']].append(current_s)

print(qs.values())


uq = {}
for i in frame:
    if i['TypeOfAction'] == 'Q':
        current_q = {i['QueryID'] : i['SessionID']} #Key = Query, Value = Session ---> current_q[Query_id] = session_id
        for u in i['ListOfURLs']:
            if u not in uq.keys():
                uq[u] = {i['QueryID'] : [i['SessionID']]}
            if u in uq.keys():
                if i['QueryID'] in uq[u].keys():
                    if i['SessionID'] not in uq[u][i['QueryID']]:
                        uq[u][i['QueryID']].append(i['SessionID'])











sc = {} #key = Session ID, value = clicked rank

for i in frame:
    if i["SessionID"] not in sc.keys():
        sc[i['SessionID']] = [] #Empty if session does not result in click

    if i['TypeOfAction'] == 'Q':
        current_q = {"SessionID": i["SessionID"], "ListOfURLs": i["ListOfURLs"][:6]}

    if i['TypeOfAction'] == 'C':

        for e in enumerate(current_q["ListOfURLs"]):
            if e[1] == i["URLID"]:
                rank = e[0]+1

        sc[i['SessionID']].append(rank) #The rank of the url id clicked in the given session


# print(len(list(sc.keys())),'sc should be 11717')

###############################################################################################

def get_sessions_per_query(data):
    """
    :param data - in the form of a list of libraries
    :return - library where key = Query ID, value = (Session IDs, list of URLs)
    """
    qs = {}
    for i in frame:
        if i['TypeOfAction'] == 'Q':
            if i['QueryID'] not in qs.keys():
                qs[i['QueryID']] = ([i['SessionID']], i['ListOfURLs'])
            elif i['QueryID'] in qs.keys():
                qs[i['QueryID']][0].append(i['SessionID'])
    return qs




def get_clicks_per_session(data):
    """
    :param data - in the form of a list of libraries
    :return - library where key = Session ID, value = clicked rank
    """
    sc = {}
    for i in data:
        if i["SessionID"] not in sc.keys():
            sc[i['SessionID']] = [] #Empty if session does not result in click
        if i['TypeOfAction'] == 'Q':
            current_q = {"SessionID": i["SessionID"], "ListOfURLs": i["ListOfURLs"][:6]}
        if i['TypeOfAction'] == 'C':
            for e in enumerate(current_q["ListOfURLs"]):
                if e[1] == i["URLID"]:
                    rank = e[0]+1
            sc[i['SessionID']].append(rank) #The rank of the url id clicked in the given session
    return sc



# def EMiter():
#     # epsilon =  1e-6
#     alphas = []
#     gammas = []
#     for i in







# def EMtrain():
#
#     convergence_eps = 0.01
