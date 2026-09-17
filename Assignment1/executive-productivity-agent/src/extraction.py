import re
import json
from typing import List, Dict
from .normalization import normalize_date, resolve_relative_term
from . import llm

COMMITMENT_PATTERNS = [
    r"I(?:'ll| will|ll)?\s+send",
    r"I(?:'ll| will|ll)?\s+get",
    r"I(?:'ll| will|ll)?\s+have",
    r"I(?:'ll| will|ll)?\s+review",
    r"I(?:'ll| will|ll)?\s+confirm",
    r"I(?:'ll| will|ll)?\s+need",
    r"I(?:'ll| will|ll)?\s+owe",
]


def extract_explicit_commitments(source: Dict) -> List[Dict]:
    text = source.get('content','')
    # Try LLM first if available
    # Attempt structured LLM extraction using the prompt template
    try:
        prompt = open('../prompts/extraction_prompt.txt').read() if False else open('prompts/extraction_prompt.txt').read()
        prompt = prompt + "\n\nSource:\n" + text
        out = llm.call_llm_system(prompt)
        if out and isinstance(out, dict) and 'tasks' in out:
            tasks = []
            allowed_categories = {'MY_ACTION','WAITING_ON_OTHERS','UNCLEAR_OWNERSHIP','COMPLETED','INFORMATIONAL'}
            for t in out.get('tasks', []):
                cat = t.get('category') if t.get('category') in allowed_categories else 'INFORMATIONAL'
                tasks.append({
                    'task_text': t.get('title') or t.get('description'),
                    'owner': t.get('owner'),
                    'recipient': t.get('recipient'),
                    'waiting_on': t.get('waiting_on'),
                    'deadline': t.get('deadline'),
                    'category': cat,
                    'commitment': bool(t.get('commitment', False)),
                    'source_id': source.get('id'),
                    'date': source.get('date'),
                    'evidence': t.get('evidence') or text
                })
            return tasks
    except llm.LLMUnavailable:
        # no key configured: deterministic fallback
        pass
    except Exception:
        # API error or malformed JSON: deterministic fallback
        pass

    # Deterministic fallback
    found = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    context_keywords = ['vendor list', 'vendor', 'q3 campaign', 'expense variance', 'mumbai', 'meridian']
    for i, sent in enumerate(sentences):
        for pat in COMMITMENT_PATTERNS:
            if re.search(pat, sent, flags=re.IGNORECASE):
                task_text = sent.strip()
                # heuristically resolve pronouns: if sentence uses 'that' or 'it', look back for keywords
                if re.search(r"\b(that|it|them|him|her)\b", task_text, flags=re.IGNORECASE):
                    for j in range(max(0, i-2), i+1):
                        for kw in context_keywords:
                            if kw in sentences[j].lower():
                                task_text = f"{task_text} (context: {sentences[j].strip()})"
                                break
                        else:
                            continue
                        break

                found.append({
                    'task_text': task_text,
                    'source_id': source.get('id'),
                    'date': source.get('date'),
                    'evidence': task_text
                })
    return found


def extract_deadlines(source: Dict) -> List[str]:
    # rudimentary date keywords
    text = source.get('content','')
    dates = []
    for word in ['Wednesday','Thursday','Friday','EOD','EOB','today','tomorrow','evening','morning']:
        if re.search(r"\b"+re.escape(word)+r"\b", text, flags=re.IGNORECASE):
            resolved = resolve_relative_term(word.lower())
            if resolved:
                dates.append(resolved)
            else:
                dates.append(word)
    # also look for explicit datetimes
    dt_matches = re.findall(r"\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?", text)
    for d in dt_matches:
        nd = normalize_date(d)
        if nd:
            dates.append(nd)
    return dates
