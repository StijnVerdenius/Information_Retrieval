
from ir_step import IRStep
from models.interleavings.prob_interleaving import ProbabilisticInterleaving
from models.interleavings.teamdraft_interleaving import TeamDraftInterleaving
from utils import softmax
from scipy.stats import norm
from saver import Saver

class InterleavingsStep(IRStep):

    def __init__(self, name, purpose, data):
        self.distribution = []
        super().__init__(name, purpose, data)

    def onStart(self, input_list):

        saver = Saver("data/")

        try:

            return_dict = saver.load_python_obj("interleavings")
            return return_dict
        except:


            probabilistic_interleavings_list = []
            team_draft_interleavings_list = []
            self.distribution = softmax([norm.pdf(x, 0, 1.5) for x in range(3)])

            for number, category in enumerate(input_list.values()):
                print ("\nStart interleaving category {}".format(number))

                local_probabilistic_interleavings_list = []
                local_team_draft_interleavings_list = []


                for pair_number, (ranking1, ranking2) in enumerate(category):

                    if (pair_number % (int(len(category))/10) == 0):
                        print("\r{} out of {} done".format(pair_number,  len(category)), end='')

                    try:
                        probabilistic_interleaving = ProbabilisticInterleaving(ranking1, ranking2, self.distribution)
                        probabilistic_interleaving.cut_off_at(3)
                        local_probabilistic_interleavings_list.append(probabilistic_interleaving)
                    except:
                        pass

                    try:
                        draft_interleaving = TeamDraftInterleaving(ranking1, ranking2)
                        draft_interleaving.cut_off_at(3)
                        local_team_draft_interleavings_list.append(draft_interleaving)
                    except:
                        pass

                probabilistic_interleavings_list.append(local_probabilistic_interleavings_list)
                team_draft_interleavings_list.append(local_team_draft_interleavings_list)

            print("\n\n")

            return_dict = {"probabilistic": probabilistic_interleavings_list, "team_draft": team_draft_interleavings_list}
            saver.save_python_obj(return_dict, "interleavings")
            return return_dict

    def onfinish(self):
        print("finished step {}".format(self.name))
