# Executive Productivity Agent

## 1. Overview

The Executive Productivity Agent ingests an executive data pack (meeting transcripts, email threads, calendar events, and voice notes), extracts commitments and deadlines, consolidates duplicates, applies deterministic business rules for deadlines and ownership, and generates an evidence-grounded daily action brief and Q&A interface.

## 2. Assignment Objective

This implementation satisfies the assignment by producing a clickable prototype that:
- Identifies explicit commitments from source materials.
- Preserves source evidence and chronology.
- Applies deterministic rules for date handling, deadline status, and ownership protection.
- Uses OpenAI for semantic extraction and concise answer formulation when available, with strict deterministic fallbacks.

## 3. Features

- Commitment identification
- My Actions
- Waiting on Others
- Deadline detection
- Overdue detection
- Deduplication
- Ownership ambiguity detection
- Daily Action Brief
- Natural-language Q&A
- Evidence/source traceability
- Demo date selector
- OpenAI + deterministic fallback

## 4. Architecture

Data Sources
↓
Ingestion
↓
LLM Extraction
↓
Validation
↓
Normalization
↓
Deduplication
↓
Deadline/Status Engine
↓
Task Store
↓
Daily Brief
↓
Q&A
↓
Streamlit UI

(See `docs/architecture.png` for a diagram.)

## 5. Technology Stack

- Python 3.13
- Streamlit (UI)
- OpenAI (optional, semantic extraction and Q&A)
- SQLite (basic storage; optional)
- pytest (tests)

## 6. AI Tools

- OpenAI API (when `OPENAI_API_KEY` is present)
	- Semantic extraction: structured JSON extraction of commitments
	- Evidence-grounded Q&A: answer formulation based on provided evidence bundle

Deterministic Python logic (always authoritative):
- Date parsing and normalization
- Deadline and status calculation
- Deduplication and latest-source resolution
- Ownership protection (do not infer owners when unclear)

## 7. Data Sources

The implementation uses only the Data Pack sources provided in `data/demo_data.json`:
- Leadership Sync transcript
- Calendars
- Email threads
- Voice notes
- People/contact information

## 8. Data-Grounding Rules

The system is evidence-grounded and will not invent facts not present in the Data Pack. LLM outputs are validated and rejected if they do not conform to expected structured JSON. Deterministic rules take precedence for date/status/ownership decisions.

## 9. Ownership Handling

Example: Mumbai Office Lease Renewal — ownership is displayed as unclear and the UI shows all supporting sources. The system does NOT guess or assign a presumed owner.

## 10. Deduplication

Vendor list commitments are deduplicated across sources; merged tasks preserve all source evidence and prefer fields from the latest source date when conflicts exist.

## 11. Latest Information

Later information supersedes earlier fields (owner, deadline) during merging while preserving historical evidence and `source_dates`.

## 12. Installation

```powershell
C:/Python313/python.exe -m pip install -r requirements.txt
```

## 13. Environment Variables

Create a `.env` file in the project root (do not commit). Example (`.env.example` provided):

```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

The app will run in deterministic demo mode if `OPENAI_API_KEY` is not set.

## 14. Running the Application

```powershell
$env:PYTHONPATH = "c:\Users\dwive\Music\Projects\Assignment1\executive-productivity-agent"
C:/Python313/python.exe -m streamlit run "c:\Users\dwive\Music\Projects\Assignment1\executive-productivity-agent\app.py"
```

## 15. Running Tests

```powershell
$env:PYTHONPATH = "c:\Users\dwive\Music\Projects\Assignment1\executive-productivity-agent"
C:/Python313/python.exe -m pytest -q
```

## 16. Demo Scenarios (recommended questions)

- What did I promise Raghav?
- What needs action today?
- What am I waiting on?
- Who owns the Mumbai office lease renewal?
- What happened with the Q3 campaign deck?
- Is the expense variance report complete?

## 17. Project Structure

```
[project root]
|-- app.py
|-- requirements.txt
|-- README.md
|-- data/demo_data.json
|-- src/
|   |-- ingestion.py
+|   |-- extraction.py
|   |-- deduplication.py
|   |-- deadline_engine.py
|   |-- status_engine.py
|   |-- brief_generator.py
|   |-- pipeline.py
|   |-- llm.py
|   |-- qa_agent.py
|-- tests/
|-- .gitignore
```

## 18. Testing

All project tests pass in this environment.

```
13 passed
```

## 19. Limitations

- The prototype uses demo data from `data/demo_data.json` and is not wired to live email/calendar sources.
- LLM dependency is optional and may vary in performance; deterministic fallback ensures safety.
- No authentication or multi-user features included.

## 20. Future Improvements

- Connect Gmail/Outlook and secure connectors.
- Add richer UI visualizations and task filtering.
- Expand tests to cover more LLM failure modes and edge cases.

## 21. Links

Live Demo:
[ADD LINK]

GitHub:
[ADD LINK]

Demo Video:
[ADD GOOGLE DRIVE LINK]
