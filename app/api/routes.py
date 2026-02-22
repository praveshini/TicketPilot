# fastapi routes

from fastapi import APIRouter,status,HTTPException
import logging
from app.model.model import TicketRequest, TicketResponse
from app.data.queue import ticket_queue
from app.core.classifier import TicketClassifier
from app.core.router import TicketRouter
from fastapi import Request
from collections import Counter

logger = logging.getLogger("uvicorn.error")
router=APIRouter()


@router.post("/ticket", status_code=status.HTTP_202_ACCEPTED)
async def create_ticket(
    ticket: TicketRequest,request: Request ) -> TicketResponse:

    try:
        router_service=request.app.state.router_service  # Access the router service from app state
        processed_ticket=await router_service.process(ticket)
        print(ticket_queue.queue.qsize())
        print(await ticket_queue.print_queue())
        return TicketResponse(
            ticket_id=processed_ticket.ticket_id,
            status="queued",
            message="Ticket processed and added to queue"
        )
    except Exception as e:
        logger.error(f"Failed to process ticket: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal engine error during ticket ingestion",
            status="failed",
            message="Ticket not added to queue",
        )


@router.get("/queue", status_code=status.HTTP_200_OK)
async def get_queue():
    try:
        tickets=await ticket_queue.get_tickets()
        tickets_data=[t.dict() for t in tickets]
        return {"status":"success", "queue": tickets_data, "total": len(tickets_data)}
    except Exception as e:
        logger.error(f"Failed to retrieve queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal engine error during queue retrieval",
        )
