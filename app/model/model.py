# json structure for ticket data and model outputs


from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional


class TicketRequest(BaseModel):
    subject: str=Field(..., min_length=5, max_length=50)
    body: str= Field(..., min_length=10, max_length=1000)
    type: str= Field(..., regex=r"^(incident|request|bug)$", description="Type of ticket")
    tag1: Optional[str] = Field(None, max_length=20)
    tag2: Optional[str] = Field(None, max_length=20)
    tag3: Optional[str] = Field(None, max_length=20)


'''MILESTONE 1'''
'''Ticket classified and processed by the ML model, ready to be added to the queue'''
class ProcessedTicket(TicketRequest):
    ticket_id: str=  Field(...,
        regex=r"^TIC-[A-Z0-9]{8}$",
        min_length=12,
        max_length=12,
        description="Unique ID in the format TIC-XXXXXXXX where X is an uppercase letter or digit",
    )
    priority: int=Field(..., ge=0, le=1)
    category: str
    created_at: datetime=  Field(default_factory=datetime.now)

'''Response model for milestone 1 - after ticket is processed and added to queue'''
class TicketResponse(BaseModel):
    ticket_id: str = Field(
        ...,
        regex=r"^TIC-[A-Z0-9]{8}$",
        min_length=12,
        max_length=12,
        description="Unique ID in the format TIC-XXXXXXXX where X is an uppercase letter or digit",
    )
    status: str= Field(..., regex=r"^(queued|processing|completed|failed)$", description="Status of the ticket in the queue")
    message: str=Field(..., min_length=10, max_length=200)


'''MILESTONE 2'''

class ProcessedTicketM2(TicketRequest):
    ticket_id: str = Field(
        ...,
        regex=r"^TIC-[A-Z0-9]{8}$",
        min_length=12,
        max_length=12,
        description="Unique ID in the format TIC-XXXXXXXX where X is an uppercase letter or digit",
    )
    category: str
    created_at: datetime = Field(default_factory=datetime.now)
    urgency: float=Field(..., ge=0.0, le=1.0, description="Urgency score between 0 and 1")
