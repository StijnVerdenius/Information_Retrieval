import utils

class Experiment():
    k = 100

    def __init__(self, interleaving_interval_lists, click_model, gammas):
        self.win_percentage = {}

        self.interleaving_interval_lists = interleaving_interval_lists
        self.click_model = click_model
        self.gammas = gammas

    def run(self):
        # self.win_percentage = utils.initialize_err_table()
        wins = 0

        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interleaving_lists in self.interleaving_interval_lists:
            for interleaving in interleaving_lists:
                for _ in range(self.k):
                    # interleaved_list = self.interleaving_model(ranking_pair)
                    # result = self.click_model(interleaved_list)
                    self.click_model(interleaving, self.gammas)

                    score = interleaving.get_score()
                    print(score)
                    # TODO: calculate the result from the click model
                    # if result:
                    #     wins += 1 # TODO: use the interleaving api instead of counting wins yourself
                
            # current_interval_pairs_length = len(self.err_table[interval_key])
            # self.win_percentage[interval_key] = wins / (self.k * current_interval_pairs_length) # TODO: use the interleaving api instead of counting wins yourself
        
        return self.win_percentage # TODO: use the interleaving api instead of counting wins yourself