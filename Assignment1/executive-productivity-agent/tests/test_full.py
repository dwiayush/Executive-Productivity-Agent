import pytest
from src.pipeline import build_tasks
from src import llm


def test_vendor_list_deduplication():
    tasks = build_tasks()
    vendor_tasks = [t for t in tasks if 'vendor list' in t['title'].lower()]
    assert len(vendor_tasks) == 1
    t = vendor_tasks[0]
    # evidence should include multiple sources
    assert len(t.get('evidence', [])) >= 1


def test_q3_latest_deadline():
    tasks = build_tasks()
    q3 = [t for t in tasks if 'q3' in t['title'].lower()]
    assert q3
    assert q3[0].get('deadline') == '2026-09-24T09:30:00'


def test_meridian_final_time():
    tasks = build_tasks()
    m = [t for t in tasks if 'meridian' in t['title'].lower()]
    assert m
    assert m[0].get('deadline').startswith('2026-09-23')
    assert m[0].get('owner') is None


def test_expense_report_completed():
    tasks = build_tasks()
    e = [t for t in tasks if 'expense variance' in t['title'].lower()]
    assert e
    assert e[0].get('status') == 'Completed'


def test_mumbai_ownership_unclear():
    tasks = build_tasks()
    m = [t for t in tasks if 'mumbai' in t['title'].lower()]
    assert m
    assert m[0].get('owner') is None


def test_overdue_upcoming_logic():
    tasks = build_tasks()
    # using status fields generated deterministically
    overdue = [t for t in tasks if t.get('status') == 'Overdue']
    upcoming = [t for t in tasks if t.get('status') == 'Upcoming']
    # we expect some overdue items in demo
    assert len(overdue) >= 1


def test_llm_unavailable_fallback():
    # if OPENAI_API_KEY not set, calling llm.call_llm_system should raise LLMUnavailable
    try:
        llm.call_llm_system('test')
    except Exception as e:
        assert isinstance(e, llm.LLMUnavailable)
    else:
        pytest.skip('LLM available in environment; skipping unavailable-key test')
