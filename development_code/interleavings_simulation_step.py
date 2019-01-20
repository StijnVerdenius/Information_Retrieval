from ir_step import IRStep
from models.experiment import Experiment

class InterleavingSimulationStep(IRStep):
    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        interleaving_model_1 = input_list[0]
        interleaving_model_2 = input_list[1]

        click_model_1 = input_list[2]
        click_model_2 = input_list[3]

        err_table = input_list[4]

        experiment_1 = Experiment(interleaving_model_1, click_model_1)
        experiment_2 = Experiment(interleaving_model_1, click_model_2)
        experiment_3 = Experiment(interleaving_model_2, click_model_1)
        experiment_4 = Experiment(interleaving_model_2, click_model_2)

        result_1 = experiment_1.run()
        result_2 = experiment_2.run()
        result_3 = experiment_3.run()
        result_4 = experiment_4.run()

        # TODO: Combine the results
        result = {}
        return result

    def onfinish(self):
        print("finished step {}".format(self.name))