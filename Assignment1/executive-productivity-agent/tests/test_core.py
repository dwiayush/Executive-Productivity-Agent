import pytest
from src.ingestion import load_demo_data
from src.extraction import extract_explicit_commitments, extract_deadlines
from src.deduplication import deduplicate
from src.deadline_engine import is_overdue, is_upcoming


def test_ingestion_and_extraction():
    data = load_demo_data('data/demo_data.json')
    sources = data.get('sources', [])
    assert len(sources) >= 1
    commits = extract_explicit_commitments(sources[0])
    assert isinstance(commits, list)


def test_deduplication():
    tasks = [
        {'title':'Send updated vendor list to Raghav','sources':['A'], 'evidence':'a'},
        {'title':'send updated vendor list to raghav','sources':['B'], 'evidence':'b'}
    ]
    unique = deduplicate(tasks)
    assert len(unique) == 1


def test_deadline_detection():
    assert is_upcoming('2026-09-24')
    assert is_overdue('2026-09-20')
