# entry point for the application, setting up the FastAPI app

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse



from app.core.classifier import TicketClassifier
from app.core.router import TicketRouter
from app.data.queue import ticket_queue
from app.api.routes import router as ticket_router


app=FastAPI(title="TicketPilot", description="A ticketing engine for IT support", version="1.0.0")

#  Configure CORS
# allows other apps to talk to the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router,tags=["tickets"])

@app.on_event("startup")
async def startup_event():
    # Initialize core components and services
    global router_service
    classifier = TicketClassifier()
    router_service = TicketRouter(classifier, ticket_queue)
    app.state.router_service = router_service  # Store in app state for access in routes
    print("ROUTER INITIALIZED")

# Health Check
@app.get("/", tags=["health"])
async def health_check():
    return {"status": "success", "message": "TicketPilot is running"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Log the real error for yourself (Lead Designer)
    print(f"Internal Validation Error: {exc.errors()}")
    
    # Return a clean, professional message to the User
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": "Invalid ticket format. Please check your fields (type, subject, etc.) and try again.",
        },
    )


if __name__ == "__main__":
    import uvicorn

    # entry point if the file is run directly
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
