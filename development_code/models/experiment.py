import utils

class Experiment():
    k = 100

    def __init__(self, interleaving_interval_lists, click_model):
        self.win_percentage = {}
        self.interleaving_interval_lists = interleaving_interval_lists
        self.click_model = click_model

    def run(self):
        self.win_percentage = utils.initialize_err_table()
        wins = 0

        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interval_index, interleaving_lists in enumerate(self.interleaving_interval_lists):
            self.win_percentage[interval_index] = []
            for interleaving in interleaving_lists:
                wins = 0
                for _ in range(self.k):
                    self.click_model.apply(interleaving)
                    # print(interleaving.click_history)
                    # print(interleaving.get_score())
                    winner = interleaving.get_winner()
                    if winner == "E":
                        wins += 1
                
                current_pair_win_percentage = wins / self.k
                self.win_percentage[interval_index].append(current_pair_win_percentage)
        print(self.win_percentage)
        return self.win_percentage