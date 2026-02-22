# storing and managing the queue of tickets to be processed

from typing import List
from app.model.model import TicketRequest, ProcessedTicket
from app.core.interfaces import StorageInterface
import itertools
import  asyncio


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
        print(f"Adding ticket to queue with priority {ticket.priority} and counter {counter}")
        await self.queue.put((ticket.priority,counter, ticket))

    async def get_tickets(self)->List:
        tickets=list(self.queue._queue)
        await asyncio.to_thread(tickets.sort, key=lambda x: (x[0], x[1]))

        return tickets

    # for debugging purposes
    async def print_queue(self):
        tickets=await self.get_tickets()

        print("Current Queue:")
        for t in tickets:
            print(f"ID: {t[2].ticket_id} | Urgency: {t[2].priority} | Created At: {t[2].created_at}")


ticket_queue=TicketQueue()        
