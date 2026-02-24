# ml models and classifying tickets

import uuid
import httpx
import re


from  app.model.model import TicketRequest, ProcessedTicket
from app.core.interfaces import ClassifierInterface



class TicketClassifier(ClassifierInterface):
    def generate_ticket_id(self) -> str:
        ticket_id = f"TIC-{uuid.uuid4().hex[:8].upper()}"
        return ticket_id
    
    
    async def api_predict(self,ticket:  TicketRequest):
        payload = ticket.dict()
        api_url ="https://22pc05-support-ticket-router-api.hf.space/predict"
        # 2. Make the asynchronous call to your FastAPI endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                # Extract data from your API response
                category = result.get("prediction")
               
            else:
                # Fallback logic if API fails
                category = "other"
                
        return category
    
    async def calculate_priority(self,body):
        urgency_pattern = r"(broken|asap|urgent|critical|emergency|failed|fail|failure|down|outage|immediately|stopped working)"


        if re.search(urgency_pattern, str(body), re.IGNORECASE):
            return 0  # Urgent
        return 1 # Normal

    


    async def classify(self,ticket:  TicketRequest)-> ProcessedTicket:
        # dummy processing function to simulate ML model output
        category = await self.api_predict(ticket)
        priority = await self.calculate_priority(ticket.body)
        return ProcessedTicket(
            ticket_id=self.generate_ticket_id(),
            subject=ticket.subject, 
            body=ticket.body,
            type=ticket.type,
            tag1=ticket.tag1,   
            tag2=ticket.tag2,
            tag3=ticket.tag3,
            priority=priority,
            category=category)


