from abc   import ABC, abstractmethod
from app.model.model import TicketRequest, ProcessedTicket

class ClassifierInterface(ABC):
    @abstractmethod
    async def classify(self, ticket: TicketRequest) -> ProcessedTicket:
        pass

class StorageInterface(ABC):
    @abstractmethod
    async def add_ticket(self, ticket: ProcessedTicket):
        pass

    @abstractmethod
    async def get_tickets(self):
        pass