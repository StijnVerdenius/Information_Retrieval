import utils

class Experiment():
    k = 3000

    def __init__(self, interleaving_interval_lists, click_model):
        self.win_percentage = {}
        self.interleaving_interval_lists = interleaving_interval_lists
        self.click_model = click_model

    def run(self):
        self.win_percentage = utils.initialize_err_table()

        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interval_index, interleaving_lists in enumerate(self.interleaving_interval_lists):
            print("\rRunning interval: {} out of {}".format(interval_index, 9), end='')
            self.win_percentage[interval_index] = []
            for interleaving in interleaving_lists:

                wins = 0
                for _ in range(self.k):
                    self.click_model.apply(interleaving)

                    winner = interleaving.get_winner()
                    if winner == "E":
                        wins += 1
                
                current_pair_win_percentage = wins / self.k
                self.win_percentage[interval_index].append(current_pair_win_percentage)
        return self.win_percentage