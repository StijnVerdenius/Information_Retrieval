from ir_step import IRStep
from models.experiment import Experiment
import user_clicks_simulation_step
from saver import Saver
import multiprocessing as mp

class InterleavingSimulationStep(IRStep):
    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        probabilistic_interleavings_list = input_list[0]["probabilistic"]
        team_draft_interleavings_list = input_list[0]["team_draft"]
        probabilistic_click_model = input_list[1]["probabilistic"]
        random_click_model = input_list[1]["random"]

        experiment_1 = Experiment((probabilistic_interleavings_list), probabilistic_click_model, 1)
        experiment_2 = Experiment((probabilistic_interleavings_list), random_click_model, 2)
        experiment_3 = Experiment((team_draft_interleavings_list), probabilistic_click_model, 3)
        experiment_4 = Experiment((team_draft_interleavings_list), random_click_model, 4)

        save_and_load = Saver("data/")

        experiments = [experiment_1, experiment_2, experiment_3, experiment_4]

        ignores = []

        q = mp.Queue()

        processes = [mp.Process(target=self.experimenting, args=(exp, q)) for exp in experiments]

        results = [None] * 4

        try:
            print("Running experiments: 1/4")
            result = save_and_load.load_python_obj("experiment1")
            results[0] = result
            ignores.append(0)
        except:
            print("started multiprocessing " + str(1))
            # result_1 = experiment_1.run()
            # save_and_load.save_python_obj(result_1, "experiment_1")
            processes[0].start()

        
        try:
            print("Running experiments: 2/4")
            result = save_and_load.load_python_obj("experiment2")
            results[1] = result
            ignores.append(1)
        except:
            print("started multiprocessing " + str(2))
            # result_2 = experiment_2.run()
            # save_and_load.save_python_obj(result_2, "experiment_2")
            processes[1].start()

        try:
            print("Running experiments: 3/4")
            result = save_and_load.load_python_obj("experiment3")
            results[2] = result
            ignores.append(2)
        except:
            print("started multiprocessing " + str(3))
            # result_3 = experiment_3.run()
            # save_and_load.save_python_obj(result_3, "experiment_3")
            processes[2].start()

        try:
            print("Running experiments: 4/4")
            result = save_and_load.load_python_obj("experiment4")
            results[3] = result
            ignores.append(3)
        except:
            print("started multiprocessing " + str(4))
            # result_4 = experiment_4.run()
            # save_and_load.save_python_obj(result_4, "experiment_4")
            processes[3].start()

        for experiment_index in range(4):
            if (experiment_index in ignores):
                continue
                
            print("Attempting get\n")
            result = q.get()
            index = result["name"]
            results[index-1] = result
            del result["name"]
            print("Got {}\n".format(index))

        for i, p in enumerate(processes):
            if (i in ignores):
                continue
            print("Attempting join\n")
            p.join()
            print("joined {}\n".format(i))


        for i, res in zip([1,2,3,4], results):
            save_and_load.save_python_obj(res, "experiment{}".format(i))

        result_1, result_2, result_3, result_4 = results[0], results[1], results[2], results[3]

        print("\rRunning experiments: Done!")

        result = {"pbm" : {"probabilistic_interleaving" : result_1, "team_draft" : result_3}, "random" : {"probabilistic_interleaving" : result_2, "team_draft" : result_4}}

        return result

    def onfinish(self):
        print("finished step {}".format(self.name))

    def experimenting(self, experiment, q):
        result, file = experiment.run()
        file.write("done\n")
        file.flush()
        q.put(result)
        file.write("put_data\n")
        file.flush()
        file.close()

        return