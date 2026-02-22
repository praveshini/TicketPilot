
from  app.model.model import TicketRequest,ProcessedTicket


class TicketRouter:
    def __init__(self, classifier, storage):
        self.classifier = classifier
        self.storage = storage

    async def process(self, ticket:TicketRequest)-> ProcessedTicket:
        processed_ticket = await self.classifier.classify(ticket)
        await self.storage.add_ticket(processed_ticket)
        return processed_ticket
