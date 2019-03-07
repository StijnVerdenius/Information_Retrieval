



class Click_Model(object):

    def __init__(self, parameters, data):
        self.parameters = parameters
        self.data = data


    def train(self):
        raise NotImplementedError("to be overrided")

    def apply(self, interleaving):
        raise NotImplementedError("to be overrided")

    def get_sc(self):  # clicks for each session
        """
        :param data - in the form of a list of libraries
        :return - library where key = Session ID, value = query:[rank, url,click]
        """
        sc = {}  # key = Session ID, value = (clicked rank, url)
        current_q = {}
        for i in self.data:
            if i["SessionID"] not in sc.keys():
                sc[i['SessionID']] = {i['QueryID']: []}

            if i['TypeOfAction'] == 'Q':
                if i['QueryID'] not in sc[i["SessionID"]].keys():
                    sc[i['SessionID']][i['QueryID']] = []  # Empty if session does not result in click
                current_q = {"SessionID": i["SessionID"], "QueryID": i['QueryID'], "ListOfURLs": i["ListOfURLs"]}
                for r, u in enumerate(i["ListOfURLs"]):
                    sc[i['SessionID']][i['QueryID']].append([r + 1, u, False])
            if i['TypeOfAction'] == 'C':
                try:
                    cur_q = current_q["ListOfURLs"]
                except:
                    continue
                for r, u in enumerate(cur_q):
                    if u == i["URLID"]:
                        for sublist in sc[i['SessionID']][current_q['QueryID']]:
                            if sublist[1] == u:
                                sublist[2] = True
        return sc

