# fastapi routes

from fastapi import APIRouter,status,HTTPException
import logging
from app.model.model import TicketRequest, TicketResponse
from app.core.classifier import TicketClassifier
from app.core.router import TicketRouter
from app.utils.simulator import run_simulator
from fastapi.responses import FileResponse
from datetime import datetime
from fastapi import Request
from collections import Counter
import asyncio


logger = logging.getLogger("uvicorn.error")
router=APIRouter()


@router.post("/ticket", status_code=status.HTTP_202_ACCEPTED)
async def create_ticket(
    ticket: TicketRequest,request: Request ) -> TicketResponse:

    try:
        router_service=request.app.state.router_service  # Access the router service from app state
        ticket_queue=request.app.state.router_service.storage  # Access the ticket queue from router service
        processed_ticket=await router_service.process(ticket)
        # print(ticket_queue.queue.qsize())
        # print(await ticket_queue.print_queue())
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
async def get_queue(request: Request):
    try:
        router_service=request.app.state.router_service  # Access the router service from app state
        ticket_queue=request.app.state.router_service.storage  # Access the ticket queue from router service
        tickets=await ticket_queue.get_tickets()
        tickets_data = await asyncio.to_thread(
            lambda: [t[2].dict() for t in tickets] #
        )       
        return {"status":"success", "queue": tickets_data, "total": len(tickets_data)}
    except Exception as e:
        logger.error(f"Failed to retrieve queue: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal engine error during queue retrieval",
        )


@router.post("/simulate", status_code=status.HTTP_200_OK)
async def trigger_simulator():
    """
    Triggers the external simulator script located in the scripts folder.
    """
    try:
        # run_simulator()
        

        return {"status": "success", "message": "Simulation sequence initiated."}
    except Exception as e:
        logger.error(f"Simulator Trigger Failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not start simulator.")


@router.get("/export")
async def export_queue_to_csv(request: Request):
    """
    Generates a CSV of the current Priority Queue state.
    """
    try:
        # Pulling from the shared Singleton instance in app.state
        router_service = request.app.state.router_service
        ticket_queue = router_service.storage
        tickets = await ticket_queue.get_tickets()

        if not tickets:
            return {"status": "empty", "message": "No data to export."}

        # data = await asyncio.to_thread(
        #     lambda: [t[2].dict() for t in tickets]  
        
        # df = pd.DataFrame(data)

        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"ticket_audit_{timestamp}.csv"

        # df.to_csv(filename, index=False)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ticket_audit_{timestamp}.txt"
        with open(filename, "w") as f:
            for t in tickets:
                f.write(f"{t[2].ticket_id}, {t[2].subject}, {t[2].priority}, {t[2].created_at}\n")
        f.close()

        return FileResponse(
            path=filename, 
            filename=filename, 
            media_type="text/csv",
            background=None 
        )
    except Exception as e:
        logger.error(f"Export Operation Failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Export failed. Please try again later.")
