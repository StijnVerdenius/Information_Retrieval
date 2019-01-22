
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
        self.distribution = softmax([norm.pdf(x.relevance_to_int(), 0, 1.5) for x in input_list[3][0][0]])
        print(self.distribution)

        # todo: agree on input-output
        # todo: cutoff?
        for category in input_list.values():
            local_probabilistic_interleavings_list = []
            local_team_draft_interleavings_list = []
            for ranking1, ranking2 in category:
                local_probabilistic_interleavings_list.append(ProbabilisticInterleaving(ranking1, ranking2, self.distribution))
                local_team_draft_interleavings_list.append(TeamDraftInterleaving(ranking1, ranking2))
            probabilistic_interleavings_list.append(local_probabilistic_interleavings_list)
            team_draft_interleavings_list.append(local_team_draft_interleavings_list)

        return {"probabilistic": probabilistic_interleavings_list, "team_draft": team_draft_interleavings_list}

    def onfinish(self):
        print("finished step {}".format(self.name))
