from datetime import datetime
import glob
import json
import os
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Event(BaseModel):
    customer_id: int
    event_type: str
    timestamp: str
    email_id: int
    clicked_link: str = None
    product_id: int = None
    amount: float = None


class ParsedEvent(BaseModel):
    customer_id: int
    event_type: str
    timestamp: datetime
    email_id: int
    clicked_link: Optional[str] = [None]
    product_id: Optional[int] = None
    amount: Optional[float] = None


@app.get("/customer_events")
async def read_customer_events(customer_id: int) -> list[ParsedEvent]:
    # TODO add optional filtering based on given time range
    files = glob.glob(f'data/parsed/customer_id_{customer_id}_*.json')
    parsed_events = []
    for file in files:
        with open(file, 'r') as f:
            event_json = f.read()  # read file content
            event = json.loads(event_json)  # load json from the string
            timestamp_str = event.get("timestamp")
            try:
                event["timestamp"] = datetime.strptime(timestamp_str, "%d-%m-%YT%H:%M:%S")
            except ValueError:
                event["timestamp"] = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
            parsed_event = ParsedEvent(**event)
            parsed_events.append(parsed_event)
    if not parsed_events:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} is not found")
    return parsed_events


@app.post("/event")
async def create_event(event: Event):
    customer_id = event.customer_id
    unique_id = uuid.uuid4()

    filename = f"customer_id_{customer_id}_{unique_id}.json"
    filepath = os.path.join("data", "parsed", filename)

    with open(filepath, 'w') as f:
        event_dict = event.model_dump(mode="json")
        json.dump(event_dict, f)

    return event
