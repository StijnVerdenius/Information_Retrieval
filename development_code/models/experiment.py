import utils

class Experiment():
    k = 3000

    def __init__(self, interleaving_interval_lists, click_model, name):
        self.win_percentage = {}
        self.interleaving_interval_lists = interleaving_interval_lists
        self.click_model = click_model
        self.name = name

    def run(self):
        self.win_percentage = utils.initialize_err_table()

        f = open("data/temp/progressfile_{}.txt".format(self.name), "w")


        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interval_index, interleaving_lists in enumerate(self.interleaving_interval_lists):

            f.write("INTERVAL" + str(interval_index) + "\n")
            f.flush()

            self.win_percentage[interval_index] = []
            for interleaving_index, interleaving in enumerate(interleaving_lists):

                try:
                    f.write("#" + str(interleaving_index) + " out of {} in bin {}\n".format(str(len(interleaving_lists)), str(interval_index)))
                    f.flush()

                    wins = 0
                    for _ in range(self.k):
                        self.click_model.apply(interleaving)

                        winner = interleaving.get_winner()
                        if winner == "E":
                            wins += 1

                    current_pair_win_percentage = wins / self.k
                    self.win_percentage[interval_index].append(current_pair_win_percentage)

                except:
                    continue

        self.win_percentage["name"] = self.name
        f.flush()
        return self.win_percentage, f