from ir_step import IRStep
from models.document import Document
import utils

class ERRStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)

    def onStart(self, ranking_pairs):
        err_table = utils.initialize_err_table()
        
        counter = 0
        for ranking_pair in ranking_pairs:
            p_err = self.calculate_err(ranking_pair[0])
            e_err = self.calculate_err(ranking_pair[1])

            difference = e_err - p_err
            
            # if E does not outperform P, discard this pair
            if difference <= 0:
                continue
            
            counter += 1
            err_table_position = utils.difference_to_err_table_position(difference)
            err_table[err_table_position].append(ranking_pair)

        print (f'total ranking pairs left: {counter}')
        
        # todo: agree on input-output (see step 3)
        return err_table

    def onfinish(self):
        print("finished step {}".format(self.name))

    def calculate_err(self, documents: [Document]):
        err_score = 0

        for r, document in enumerate(documents):
            inner_result = 1
            
            if r > 0:
                for i in range(r - 1):
                    inner_result *= (1 - documents[i].relevance_to_int())
            
            err_score = inner_result * document.relevance_to_int()
            err_score /= (r + 1)
        
        return err_score