
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

        self.distribution = softmax([norm.pdf(x, 0, 1.5) for x in range(input_list[1])])

        print(self.distribution)

        # todo: agree on input-output
        # todo: cutoff?
        for category in input_list[0]:
            for ranking1, ranking2 in category:
                probabilistic_interleavings_list.append(ProbabilisticInterleaving(ranking1, ranking2, self.distribution))
                team_draft_interleavings_list.append(TeamDraftInterleaving(ranking1, ranking2))

        return {"probabilistic": probabilistic_interleavings_list, "team_draft": team_draft_interleavings_list}

    def onfinish(self):
        print("finished step {}".format(self.name))
