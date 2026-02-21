# json structure for ticket data and model outputs

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# trial version of the ticket data structure
class TicketRequest(BaseModel):
    ticket_id: str
    subject: str
    body: str



