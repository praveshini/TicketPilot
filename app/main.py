# entry point for the application, setting up the FastAPI app

from fastapi import FastAPI

app=FastAPI(title="TicketPilot", description="A ticketing engine for IT support", version="1.0.0")

if __name__ == "__main__":
    import uvicorn

    # Tentry point if the file is run directly
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
