from ir_step import IRStep
from models.experiment import Experiment
import user_clicks_simulation_step

class InterleavingSimulationStep(IRStep):
    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        probabilistic_interleavings_list = input_list[0]["probabilistic"]
        team_draft_interleavings_list = input_list[0]["team_draft"]
        probabilistic_click_model = input_list[1]["probabilistic"]
        random_click_model = input_list[1]["random"]

        experiment_1 = Experiment(probabilistic_interleavings_list, probabilistic_click_model)
        experiment_2 = Experiment(probabilistic_interleavings_list, random_click_model)
        experiment_3 = Experiment(team_draft_interleavings_list, probabilistic_click_model)
        experiment_4 = Experiment(team_draft_interleavings_list, random_click_model)

        # print("\rRunning experiments: 1/4", end='')
        result_1 = experiment_1.run()
        # print("\rRunning experiments: 2/4", end='')
        result_2 = experiment_2.run()
        # print("\rRunning experiments: 3/4", end='')
        result_3 = experiment_3.run()
        # print("\rRunning experiments: 4/4", end='')
        result_4 = experiment_4.run()
        # print("\rRunning experiments: Done!")

        # TODO: Combine the results
        result = {"pbm" : {"probabilistic_interleaving" : result_1, "team_draft" : result_3}, "random" : {"probabilistic_interleaving" : result_2, "team_draft" : result_4}}
        return result

    def onfinish(self):
        print("finished step {}".format(self.name))