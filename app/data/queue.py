# storing and managing the queue of tickets to be processed

import asyncio
from typing import List
from app.model.model import TicketRequest, ProcessedTicket
from app.core.interfaces import StorageInterface
import itertools


class TicketQueue(StorageInterface):
    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TicketQueue, cls).__new__(cls)
            cls._instance.queue = asyncio.PriorityQueue()
            cls._instance._counter = itertools.count()            
            print("TICKET QUEUE CREATED!")
        return cls._instance

    async def add_ticket(self,ticket: ProcessedTicket):
        counter=next(self._counter)
        await self.queue.put((ticket.urgency,counter, ticket))

    async def get_tickets(self)-> List[ProcessedTicket]:
        tickets=list(self.queue._queue)
        tickets.sort()
        return [ticket[2] for ticket in tickets]

    # for debugging purposes
    async def print_queue(self):
        tickets=await self.get_tickets()

        print("Current Queue:")
        for t in tickets:
            print(f"ID: {t.ticket_id} | Urgency: {t.urgency} | Created At: {t.created_at}")


ticket_queue=TicketQueue()        
