# ml models and classifying tickets

import uuid

from  app.model.model import TicketRequest, ProcessedTicket
from app.data.queue import ticket_queue
from app.core.interfaces import ClassifierInterface



class TicketClassifier(ClassifierInterface):
    def generate_ticket_id(self) -> str:
        ticket_id = f"TIC-{uuid.uuid4().hex[:8].upper()}"
        return ticket_id



    async def classify(self,ticket:  TicketRequest)-> ProcessedTicket:
        # dummy processing function to simulate ML model output
        return ProcessedTicket(
            ticket_id=self.generate_ticket_id(),
            subject=ticket.subject, 
            body=ticket.body,
            type=ticket.type,
            tag1=ticket.tag1,   
            tag2=ticket.tag2,
            tag3=ticket.tag3,
            urgency=0.75,
            priority=2,
            category="billing")

