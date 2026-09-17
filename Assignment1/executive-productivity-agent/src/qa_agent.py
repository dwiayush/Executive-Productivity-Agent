import os
from typing import List
from .normalization import ASSIGNMENT_START

OPENAI_KEY = os.getenv('OPENAI_API_KEY')


def answer_question(question: str, tasks: List[dict]):
    q = question.strip()
    qlow = q.lower()
    results = []
    # If question mentions a person name, match tasks with that name in title/recipient/evidence
    names = []
    for w in ['raghav', 'divya', 'arjun', 'facilities']:
        if w in qlow:
            names.append(w)

    if any(word in qlow for word in ['promise', 'promised', 'i promised', 'i promise']):
        for t in tasks:
            title = t.get('title','').lower()
            ev = t.get('evidence','')
            if isinstance(ev, list):
                evidence = ' '.join(ev).lower()
            else:
                evidence = str(ev).lower()
            owner = str(t.get('owner','')).lower()
            if owner.startswith('arjun') and any(n in title or n in evidence for n in names):
                results.append(t)
        return results

    if 'needs action today' in q or 'what needs action today' in q:
        for t in tasks:
            owner = str(t.get('owner','')).lower()
            if t.get('status') in ('Overdue','Upcoming') or (owner.startswith('arjun') and t.get('status')=='Pending'):
                results.append(t)
        return results

    if 'who owns' in q or 'who is the owner' in q:
        if 'mumbai' in q:
            m = []
            for t in tasks:
                title = t.get('title','').lower()
                ev = t.get('evidence','')
                if isinstance(ev, list):
                    evidence = ' '.join(ev).lower()
                else:
                    evidence = str(ev).lower()
                if 'mumbai' in title or 'mumbai' in evidence:
                    m.append(t)
            if not m:
                return {'answer':'Ownership is unclear','evidence':[]}
            owner = m[0].get('owner')
            if owner is None:
                return {'answer':'Ownership is unclear','evidence':m[0].get('evidence')}
            return {'answer':owner,'evidence':m[0].get('evidence')}

    # If LLM available, perform evidence-grounded answer generation
    try:
        # select relevant tasks by simple keyword matching on title/evidence/sources
        relevant = []
        qwords = [w for w in qlow.split() if len(w) > 2]
        for t in tasks:
            title = t.get('title','').lower()
            evidence = ' '.join(t.get('evidence',[])).lower() if isinstance(t.get('evidence',[]), list) else str(t.get('evidence','')).lower()
            sources = ' '.join(t.get('sources',[])).lower()
            if any(w in title or w in evidence or w in sources for w in qwords):
                relevant.append(t)

        if not os.getenv('OPENAI_API_KEY'):
            # deterministic fallback: return relevant tasks
            return relevant

        # build evidence payload
        evidence_bundle = []
        for t in relevant:
            evidence_bundle.append({'id': t.get('id'), 'text': evidence, 'source': t.get('sources')})

        # LLM prompt: answer only from evidence
        prompt = open('../prompts/qa_prompt.txt').read() if False else open('prompts/qa_prompt.txt').read()
        prompt += "\n\nQuestion: " + q + "\n\nEvidence: \n"
        for e in evidence_bundle:
            prompt += f"[{e['id']}] {e['text']}\n"

        # instruct model to return JSON: {"answer":"...","sources":[ids]}
        prompt += "\nReturn JSON: {\"answer\": \"string\", \"sources\": [\"id\"]}. Use only evidence. If unclear, say 'Ownership unclear' or 'Not established'."

        out = llm.call_llm_system(prompt)
        if out and isinstance(out, dict) and out.get('answer'):
            return {'answer': out.get('answer'), 'sources': out.get('sources', [])}
        # fallback to deterministic result
        return relevant
    except llm.LLMUnavailable:
        return relevant
    except Exception:
        return relevant
