
from ir_step import IRStep
from saver import Saver
from models.click_models.pbm import PBM
from models.click_models.random_click import Random_Click_Model

class UserClicksSimulationStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)


    def onStart(self, input_list):
        length_interleaving = input_list[0]
        save_and_load = Saver("data/")

        pbm_model = PBM([0.2]*length_interleaving, self.data)
        try:
            print("Attempting loading gamma's from pickle")
            gammas_pbm = save_and_load.load_python_obj("gammas_pbm")
            pbm_model.parameters = gammas_pbm
        except:
            print("Did not find gamma's saved in pickle so will retrain and save")
            pbm_model.train()
            save_and_load.save_python_obj(pbm_model.parameters, "gammas_pbm")

        random_model = Random_Click_Model([0.2] * length_interleaving, self.data)
        try:
            print("Attempting loading gamma's from pickle")
            rho_random = save_and_load.load_python_obj("rho_random")
            random_model.parameters = rho_random
        except:
            print("Did not find rho saved in pickle so will retrain and save")
            random_model.train()
            save_and_load.save_python_obj(random_model.parameters, "rho_random")

        return (pbm_model, random_model)

    def onfinish(self):
        print("finished step {}".format(self.name))



### To test step 4 uncomment:
# UserClicksSimulationStep(None, None, Saver("data/").load_data_model_1()).do_step([10])


