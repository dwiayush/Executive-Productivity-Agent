import os
import json
from typing import Optional

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')


class LLMUnavailable(Exception):
    pass


def call_llm_system(content: str, temperature: float = 0.0, max_tokens: int = 512, timeout: int = 15) -> Optional[dict]:
    """Call OpenAI ChatCompletion with system content and return JSON-parsed response.
    Raises LLMUnavailable if key missing.
    Returns None on API errors or invalid/malformed JSON.
    """
    if not OPENAI_KEY:
        raise LLMUnavailable('OpenAI API key not configured')
    try:
        import openai
        openai.api_key = OPENAI_KEY
        model = OPENAI_MODEL
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{'role': 'system', 'content': content}],
            temperature=temperature,
            max_tokens=max_tokens,
            request_timeout=timeout,
        )
        # extract assistant text
        text = resp['choices'][0]['message']['content']
        if not text or not text.strip():
            return None
        # Expect JSON
        try:
            return json.loads(text)
        except Exception:
            # try to extract JSON substring
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(text[start:end+1])
                except Exception:
                    return None
            return None
    except Exception:
        return None
