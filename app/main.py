import json
import json
import os
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

from fastapi import FastAPI

app = FastAPI()


@app.get("/customer_events")
async def read_customer_events(customer_id: int):
    return {"message": f"Customer events for customer id {customer_id} here"}


class Event(BaseModel):
    customer_id: int
    event_type: str
    timestamp: str
    email_id: int
    clicked_link: str = None
    product_id: int = None
    amount: float = None


@app.post("/events")
async def create_event(event: Event):
    customer_id = event.customer_id
    event_type = event.event_type
    unique_id = uuid.uuid4()

    filename = f"customer_id_{customer_id}_event_{event_type}_{unique_id}.json"
    filepath = os.path.join("data", "parsed", filename)

    with open(filepath, 'w') as f:
        # Serializing json
        json.dump(event.model_dump_json(by_alias=True), f)

    return event
