
from ir_step import IRStep
from models.interleavings.prob_interleaving import ProbabilisticInterleaving
from models.interleavings.teamdraft_interleaving import TeamDraftInterleaving
from utils import softmax
from scipy.stats import norm
class InterleavingsStep(IRStep):

    def __init__(self, name, purpose, data):
        self.distribution = []
        super().__init__(name, purpose, data)

    def onStart(self, input_list):

        probabilistic_interleavings_list = []
        team_draft_interleavings_list = []

        # what's supposed to be here?
        self.distribution = softmax([norm.pdf(x, 0, 1.5) for x in range(3)])
        print(self.distribution)

        # todo: agree on input-output
        # todo: cutoff?
        for number, category in enumerate(input_list.values()):
            print ("\nStart interleaving category {}".format(number))

            local_probabilistic_interleavings_list = []
            local_team_draft_interleavings_list = []


            for pair_number, (ranking1, ranking2) in enumerate(category):

                if (pair_number % (int(len(category))/10) == 0):
                    print("\r{} out of {} done".format(pair_number,  len(category)), end='')

                probabilistic_interleaving = ProbabilisticInterleaving(ranking1, ranking2, self.distribution)
                # probabilistic_interleaving.cut_off_at(3)
                local_probabilistic_interleavings_list.append(probabilistic_interleaving)

                draft_interleaving = TeamDraftInterleaving(ranking1, ranking2)
                # draft_interleaving.cut_off_at(3)
                local_team_draft_interleavings_list.append(draft_interleaving)

            probabilistic_interleavings_list.append(local_probabilistic_interleavings_list)
            team_draft_interleavings_list.append(local_team_draft_interleavings_list)

        print("\n\n")

        return {"probabilistic": probabilistic_interleavings_list, "team_draft": team_draft_interleavings_list}

    def onfinish(self):
        print("finished step {}".format(self.name))
