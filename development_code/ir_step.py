class IRStep(object):

    def __init__(self, name=None, purpose=None, data=None):
        self.name = name
        self.purpose = purpose
        self.data = data

    def do_step(self, input_list):
        print("Starting step {}".format(self.name))
        if (not self.purpose == None):
            print("Goal:" + self.purpose + "\n\n")

        self.onStart(input_list)
        self.onfinish()

    def onStart(self, input_list):
        raise Exception("method to be overrided by subclass Step#")

    def onfinish(self):
        raise Exception("method to be overrided by subclass Step#")