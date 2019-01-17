import pickle
import json

class Saver():

    def __init__(self, directory):
        self.directory = directory

    def save_python_obj(self, obj, name):
        with open(self.directory + name+".pickle", 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print("Saved {}".format(name))

    def load_python_obj(self, name):
        obj = None
        try:
            with (open(self.directory + name+".pickle", "rb")) as openfile:
                obj = pickle.load(openfile)
        except FileNotFoundError:
            raise FileNotFoundError("{} not loaded because file is missing".format(name))

        return obj

    def load_data_model_1(self):
        try:
            frame = self.load_python_obj("data_model_1")
            print("Loaded sucessfully")
            return frame
        except FileNotFoundError:

            print("Building data framework")

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

            self.save_python_obj(frame, "data_model_1")

            print("Created data model_1, this only needs to be done once")
            return frame
