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

# ---------- In‑memory storage ----------
from threading import Lock

_events: dict[str, Event] = {}
_events_lock = Lock()

# ---------- Placeholder Endpoints ----------
@app.post("/ingest")
def ingest_events(events: List[Event]):
    """Store incoming events in an in‑memory dictionary.
    In a full implementation this would persist to PostgreSQL and Neo4j.
    """
    with events_lock:
        for ev in events:
            _events[ev.id] = ev
    return {"ingested": len(events)}

@app.get("/events/{event_id}")
def get_event(event_id: str):
    """Retrieve a stored event by its ID."""
    ev = _events.get(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    return ev

def _simple_pattern_engine(target: Event) -> List[dict]:
    """Very naive pattern detector.
    Returns a list of pattern dicts where each dict contains:
    - name: str, description of the pattern
    - matches: list of event IDs that share the same domain or any tag
    """
    matches_by_domain = []
    matches_by_tag = []
    with events_lock:
        for ev in _events.values():
            if ev.id == target.id:
                continue
            if ev.domain and target.domain and ev.domain == target.domain:
                matches_by_domain.append(ev.id)
            if set(ev.tags) & set(target.tags):
                matches_by_tag.append(ev.id)
    patterns = []
    if matches_by_domain:
        patterns.append({"name": f"Same domain ({target.domain})", "matches": matches_by_domain})
    if matches_by_tag:
        patterns.append({"name": "Shared tags", "matches": matches_by_tag})
    return patterns

@app.get("/patterns/{event_id}")
def get_patterns(event_id: str):
    """Run a very simple pattern engine for the given event.
    Returns a list of detected patterns.
    """
    target = _events.get(event_id)
    if not target:
        raise HTTPException(status_code=404, detail="Event not found")
    patterns = _simple_pattern_engine(target)
    return {"event_id": event_id, "patterns": patterns}


# ---------- Run Server ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
