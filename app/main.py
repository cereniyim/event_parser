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
    """
    Reads customer events based on the given customer ID.

    Parameters
    ----------
    customer_id : int
        The ID of the customer for which to retrieve events.

    Returns
    -------
    list[ParsedEvent]
        A list of parsed events for the given customer ID.

    Note
    ----
    This method also supports optional filtering based on a given time range. However, the implementation for this
    feature is not yet available.

    Raises
    ------
    HTTPException
        If no parsed events are found for the given customer ID, a 404 status code with a corresponding error message
         will be raised.

    """
    # TODO add optional filtering based on given time range
    files = glob.glob(f"data/parsed/customer_id_{customer_id}_*.json")
    parsed_events = []
    for file in files:
        with open(file, "r") as f:
            event_json = f.read()  # read file content
            event = json.loads(event_json)  # load json from the string
            timestamp_str = event.get("timestamp")
            try:
                event["timestamp"] = datetime.strptime(
                    timestamp_str, "%d-%m-%YT%H:%M:%S"
                )
            except ValueError:
                event["timestamp"] = datetime.strptime(
                    timestamp_str, "%Y-%m-%dT%H:%M:%S"
                )
            parsed_event = ParsedEvent(**event)
            parsed_events.append(parsed_event)
    if not parsed_events:
        raise HTTPException(
            status_code=404, detail=f"Customer {customer_id} is not found"
        )
    return parsed_events


@app.post("/event")
async def create_event(event: Event) -> Event:
    """
    Parameters
    ----------
    event : Event
        The event to be created.

    Returns
    -------
    Event
        The created event.

    """
    customer_id = event.customer_id
    unique_id = uuid.uuid4()

    filename = f"customer_id_{customer_id}_{unique_id}.json"
    filepath = os.path.join("data", "parsed", filename)

    with open(filepath, "w") as f:
        event_dict = event.model_dump(mode="json")
        json.dump(event_dict, f)

    return event
