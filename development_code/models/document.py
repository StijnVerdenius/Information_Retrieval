from models.relevance import Relevance

class Document:
    
    def __init__(self, id, relevance : Relevance):
        self.id = id
        self.relevance = relevance

    def __str__(self):
        # return f'<Document (id: {self.id}, relevancy: {0 if self.relevance == Relevance.NOT_RELEVANT else 1})>'
        return str(self.id)