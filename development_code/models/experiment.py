import utils

class Experiment():
    k = 100

    def __init__(self, interleaving_interval_lists, click_model):
        self.win_percentage = {}
        self.interleaving_interval_lists = interleaving_interval_lists
        self.click_model = click_model

    def run(self):
        # self.win_percentage = utils.initialize_err_table()
        wins = 0

        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interleaving_lists in self.interleaving_interval_lists:
            for interleaving in interleaving_lists:
                for _ in range(self.k):


                    self.click_model.apply(interleaving)



                    score = interleaving.get_score()
                    print(score)

                    # question from stijn: does the score needs to be reset for every _ in self.k?


                winner = interleaving.get_winner()
                # todo: add winner to correct counter
                
            # current_interval_pairs_length = len(self.err_table[interval_key])
            # self.win_percentage[interval_key] = wins / (self.k * current_interval_pairs_length)
        
        return self.win_percentage