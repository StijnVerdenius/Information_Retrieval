import utils

class Experiment():
    k = 100

    def __init__(self, interleaving_model, click_model, err_table):
        self.win_percentage = {}

        self.interleaving_model = interleaving_model
        self.click_model = click_model
        self.err_table = err_table

    def run(self):
        self.win_percentage = utils.initialize_err_table()
        wins = 0

        # for each interval, for each ranking pair we first 
        # run interleaving model then the click model k times
        for interval_key in self.err_table.keys():
            for ranking_pair in self.err_table[interval_key]:
                for _ in range(self.k):
                    interleaved_list = self.interleaving_model(ranking_pair)
                    result = self.click_model(interleaved_list)
                    
                    # TODO: calculate the result from the click model
                    if result:
                        wins += 1
                
            current_interval_pairs_length = len(self.err_table[interval_key])
            self.win_percentage[interval_key] = wins / (self.k * current_interval_pairs_length)
        
        return self.win_percentage