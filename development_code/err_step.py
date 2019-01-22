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


            if counter >= 100:
                # for document in ranking_pair[0]:
                #     print(document)
                # print("----------------")
                # for document in ranking_pair[1]:
                #     print(document)
                break

        print (f'total ranking pairs left: {counter}')
        
        # todo: agree on input-output (see step 3)
        return err_table

    def onfinish(self):
        print("finished step {}".format(self.name))

    def calculate_err(self, documents: [Document]):
        err_score = 0

        max_relevance = 0
        for document in documents:
            document_relevance = document.relevance_to_int()
            if document_relevance > max_relevance:
                max_relevance = document_relevance

        for r, document in enumerate(documents):
            inner_result = 1
            for i in range(r):
                theta_i = (2**(documents[i].relevance_to_int()) - 1)/ (2**(max_relevance))
                inner_result *= (1 - theta_i)
        
            theta_r = (2**(document.relevance_to_int()) - 1)/ (2**(max_relevance))
            current_err_score = inner_result * theta_r
            current_err_score /= (r + 1)
            
            err_score += current_err_score
        
        return err_score