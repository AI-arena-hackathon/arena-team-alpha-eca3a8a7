# EchoPlex

Team alpha — spec §3.2 hackathon build.

**One-liner:** A web app to identify and visualize recurring patterns in historical events

**Problem:** People struggle to recognize and learn from recurring patterns in history

**Solution:** EchoPlex uses natural language processing and machine learning to identify and visualize temporal patterns, allowing users to explore and understand historical events in a new way

**Build scope:** **Leo, Pattern Historian – Day 4‑5 Architecture (EchoPlex)**  

**Tech stack**  
- **Backend:** Python 3.11, FastAPI, PostgreSQL + **Neo4j** for temporal graph storage.  
- **ML/NLP:** spaCy + Hugging‑Face Transformers (distil‑roberta‑base), Dask for batch jobs.  
- **Frontend:** React 18 with **Vega‑Lite** for timeline‑graph visualizations; Auth0 for user mgmt.  

**Three core components**  
1. **Ingestion & Normalization** – Scrapes structured sources (Wikidata, DBpedia), maps each event to a canonical schema (date, actors, domain, causal tags). Mirrors the data‑pipeline pattern used in *Google Ngram Viewer* (historical text‑frequency) but adds a graph‑ready temporal model.  
2. **Pattern Engine** – Runs a hybrid pipeline: (a) rule‑based motif detectors (e.g., “rise‑peak‑decline” cycles, echoing Kondratiev wave analysis) and (b) a fine‑tuned transformer that learns similarity embeddings across events. The dual‑approach recalls the “Histography” game’s timeline clustering while extending it with ML‑driven analogies.  
3. **Exploration UI** – Interactive timeline where users select a seed event, see “Echoes” (matched patterns) highlighted, and can toggle graph layers (political, technological, cultural). This visual metaphor is akin to *Gapminder* but oriented to pattern recurrence rather than raw metrics.  

**Top 2 risks**  
- **Historical bias / data sparsity:** Over‑representation of Western events may skew pattern detection. Mitigation: weighted sampling and provenance tags.  
-

Built entirely by an AI coding agent across discrete GitHub Actions build turns (spec §8) — no human-written code.
