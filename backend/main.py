"""FastAPI entry point for EchoPlex backend.
Provides health check and placeholder routes for ingestion, pattern engine, and event queries.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="EchoPlex Backend")

# ---------- Models ----------
class Event(BaseModel):
    id: str = Field(..., description="Unique identifier for the event")
    title: str = Field(..., description="Short human readable title")
    date: str = Field(..., description="ISO 8601 date string, e.g., 1945-05-08")
    actors: List[str] = Field(default_factory=list, description="List of involved actors/entities")
    domain: Optional[str] = Field(None, description="Domain such as politics, technology, culture")
    tags: List[str] = Field(default_factory=list, description="Causal or thematic tags")

# ---------- Health ----------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------- Placeholder Endpoints ----------
@app.post("/ingest")
def ingest_events(events: List[Event]):
    # TODO: store events in PostgreSQL and Neo4j
    return {"ingested": len(events)}

@app.get("/patterns/{event_id}")
def get_patterns(event_id: str):
    # TODO: run pattern engine and return matching patterns
    raise HTTPException(status_code=501, detail="Pattern engine not implemented yet")

# ---------- Run Server ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
