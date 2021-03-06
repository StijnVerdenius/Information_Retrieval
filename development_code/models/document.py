
class Document:
    
    def __init__(self, id, relevance : int):
        self.id = id
        self.relevance = relevance

    def __str__(self):
        return str({"relevance" : self.relevance_to_int(), "id": self.id})
        # return f'<Document (id: {self.id}, relevancy: {0 if self.relevance == Relevance.NOT_RELEVANT else 1})>'
        # return str(self.relevance)

    def relevance_to_int(self):
        return self.relevance
        # return 0 if self.relevance == Relevance.NOT_RELEVANT else 1