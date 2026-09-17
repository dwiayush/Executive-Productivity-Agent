import pytest
from src import llm
from src.pipeline import build_tasks
from src import qa_agent


def test_llm_unavailable_raises():
    # Ensure LLMUnavailable is raised when no key
    # Temporarily unset key
    orig = llm.OPENAI_KEY
    llm.OPENAI_KEY = None
    with pytest.raises(llm.LLMUnavailable):
        llm.call_llm_system('test')
    llm.OPENAI_KEY = orig


def test_llm_malformed_json_fallback(monkeypatch):
    # simulate LLM returning malformed data -> extraction should fall back
    def fake_call(prompt, *args, **kwargs):
        return {'not_tasks': []}

    monkeypatch.setattr(llm, 'call_llm_system', fake_call)
    tasks = build_tasks()
    # pipeline should still produce deterministic tasks
    assert any('vendor list' in t['title'].lower() for t in tasks)


def test_qa_llm_exception_fallback(monkeypatch):
    # simulate LLM raising exception during QA -> deterministic relevant returned
    def fake_call(prompt, *args, **kwargs):
        raise Exception('API error')

    monkeypatch.setattr(llm, 'call_llm_system', fake_call)
    tasks = build_tasks()
    res = qa_agent.answer_question('What did I promise Raghav?', tasks)
    # fallback returns list of relevant tasks
    assert isinstance(res, list)
    assert any('vendor list' in t['title'].lower() for t in res)
