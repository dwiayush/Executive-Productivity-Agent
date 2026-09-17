Defense Questions and Answers

1. Why did you use an LLM?
- To extract semantically-rich commitments and generate concise, human-friendly answers. LLMs speed up semantic parsing where rules are brittle.

2. Why not use only rules?
- Rules are reliable for deterministic parts but brittle for semantic extraction across natural language varieties; LLMs complement rules but do not replace them.

3. How do you prevent hallucination?
- LLM outputs are validated against a strict JSON schema and the system falls back to deterministic extraction if responses are invalid or missing.

4. How do you handle conflicting information?
- Deduplication merges items and prefers fields from the latest `source_dates` while preserving historical evidence.

5. How does deduplication work?
- Uses text similarity and domain-keyword heuristics to group tasks, then merges evidence and resolves fields with latest-source wins for owner/deadline.

6. How do you detect commitments?
- The system uses sentence-level heuristics as deterministic fallback and LLM-structured extraction when available.

7. How do you determine ownership?
- Extract owner mentions; if sources are ambiguous or absent, leave `owner` as `None` and flag as unclear.

8. Why is Mumbai lease ownership unclear?
- No source clearly assigns an owner; therefore the system shows ownership as unclear and displays evidence.

9. How do you calculate overdue?
- Deterministically parse ISO dates and compare against the selected `as_of` demo date; overdue if deadline < as_of.

10. Why should date calculations be deterministic?
- Dates drive actionable decisions; deterministic rules ensure reliable, explainable behavior.

11. What happens if OpenAI is unavailable?
- The system falls back to deterministic extraction and Q&A; app shows AI Mode: Deterministic Demo.

12. What happens if the LLM returns malformed JSON?
- The response is rejected and the deterministic fallback is used; tests cover malformed/exception cases.

13. How is evidence preserved?
- Each task stores `sources`, `source_dates`, and `evidence` as lists; merge preserves and flattens them.

14. How do you handle multiple sources?
- Merge similar items and attach all source evidence to the consolidated task.

15. How would you scale this system?
- Introduce incremental ingestion, a scalable database, caching, batched LLM calls, and connectors for Gmail/Calendar.

16. How would you connect Gmail/Outlook in production?
- Use OAuth2, secure connectors, granular scopes, and a data ingestion pipeline with rate limits and consent.

17. How would you protect executive data?
- Encrypt data at rest, secure API keys, role-based access control, logging, and private cloud deployment.

18. What are the current limitations?
- Demo-only data, no live connectors, limited UI polish specific to one user persona.

19. What would you improve with more time?
- Live connectors, richer entity resolution, audit trail export, email/calendar integration tests.

20. Why is this an "agent" rather than just a chatbot?
- It performs task-oriented processing: ingestion, extraction, stateful deduplication, and generates prioritized actions, not free-form chat.

(Additional follow-ups can be prepared on request.)
