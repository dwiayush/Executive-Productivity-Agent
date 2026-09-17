15-minute Demo Script

0:00–1:30 — Problem
- Introduce the challenge: fragmented inputs, missed commitments, unclear ownership.
- Quick statement of goals.

1:30–3:00 — Solution Summary
- Describe the agent and main capabilities.

3:00–5:00 — Architecture
- Walk through the `docs/architecture.mmd` flow: ingestion → LLM extraction (optional) → validation → normalization → deduplication → status engine → brief → Q&A → UI.

5:00–11:00 — Live application demo (6 minutes)
- Open the Streamlit UI.
- Show top-left: Arjun Malhotra, role; top-right: AI Mode indicator.
- Use the date selector to demonstrate different days (21–25 Sep 2026).
- Demonstrate the Daily Action Brief prioritized view:
  1. Show Overdue items
  2. Show Actions Due Today
  3. Show Unclear Ownership (Mumbai lease) and expand evidence
  4. Show Upcoming deadlines (Q3 deck on 24 Sep)
  5. Show Waiting on Others
- Q&A: use example button "What did I promise Raghav?" and show answer + supporting evidence.
- Demonstrate deterministic fallback by running without `OPENAI_API_KEY`.

11:00–13:00 — Technical implementation
- Explain extraction flow and validation, deduplication rules, and latest-source merging.

13:00–15:00 — Conclusion and defence
- Summarize key capabilities and limitations.
- Invite questions and be ready to defend design choices.
