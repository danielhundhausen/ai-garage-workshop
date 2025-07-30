from datetime import datetime
import hashlib
from typing import List, Dict
import uuid

from fastapi import FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount the static folder
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# In-memory message store
messages: List[Dict] = []

# In-memory tracking of last retrieval times per client
last_retrieval_times: Dict[str, datetime] = {}


class Message(BaseModel):
    sender: str
    content: str
    user_id: str


@app.post("/messages")
def publish_message(msg: Message):
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(),
        "sender": msg.sender,
        "content": msg.content,
        "user_id": msg.user_id,
    }
    messages.append(entry)
    return {"status": "Message published", "message": entry}


@app.get("/messages/all")
def get_all_messages():
    return messages


@app.get("/messages/new")
def get_new_messages(unique_user_id: str):
    last_seen = last_retrieval_times.get(unique_user_id, datetime(1970, 1, 1))

    now = datetime.now()
    last_retrieval_times[unique_user_id] = now

    new_messages = [msg for msg in messages if msg["timestamp"] > last_seen]
    return {"status": f"Messages since {last_seen}", "messages": new_messages}


@app.delete("/messages")
def clear_messages(pw: str = Header(...)):
    incoming_hash = hashlib.sha256(pw.encode()).hexdigest()
    if (
        incoming_hash
        != "e28b6665c9592e8c070df7cf7cfd0a3171e757b27a64b9053f116d2f7bca2b82"
    ):
        raise HTTPException(status_code=403, detail="Forbidden: Incorrect password")

    messages.clear()
    return {"status": "All messages cleared"}
