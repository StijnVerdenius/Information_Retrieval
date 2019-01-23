from ir_step import IRStep
import numpy as np
import itertools
from typing import List

from models.document import Document

class RankingsStep(IRStep):

    def __init__(self, name, purpose, data):
        super().__init__(name, purpose, data)

    def onStart(self, input_list):
        print("--- generating documents...")

        documents = self.generate_documents()

        print("--- generating rankings...")
        p_rankings = itertools.permutations(documents, r=3)
        e_rankings = itertools.permutations(documents, r=3)
        
        print("--- generating ranking pairs...")
        rankings_pairs = list(itertools.product(p_rankings, e_rankings))
        rankings_pairs = [(list(item[0]), list(item[1])) for item in rankings_pairs]

        print(f'--- finished generating {len(rankings_pairs)} ranking pairs')
                
        return rankings_pairs

    def onfinish(self):
        print("\n\nfinished step {}\n\n".format(self.name))

    def generate_documents(self) -> List[Document]:
        current_id = 1
        documents = []
        
        # create 6 NOT_RELEVANT documents 
        for i in range(3):
            documents.append(Document(current_id, 0))#Relevance.NOT_RELEVANT))
            current_id += 1

        # create 6 RELEVANT documents
        for i in range(3):
            documents.append(Document(current_id, 1))#Relevance.RELEVANT))
            current_id += 1

        return documents
