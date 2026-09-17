from dateutil import parser
from datetime import datetime

ASSIGNMENT_START = datetime(2026,9,21)
ASSIGNMENT_END = datetime(2026,9,25)


def normalize_date(date_str: str):
    try:
        dt = parser.parse(date_str, dayfirst=False)
        return dt.date().isoformat()
    except Exception:
        return None


def in_assignment_week(date_iso: str):
    if not date_iso:
        return False
    dt = parser.parse(date_iso).date()
    return ASSIGNMENT_START.date() <= dt <= ASSIGNMENT_END.date()


def resolve_relative_term(term: str):
    """Resolve relative weekday/terms to ISO date strings within the assignment week."""
    t = term.lower()
    # map weekdays to dates in assignment week
    mapping = {
        'monday': ASSIGNMENT_START.date(),
        'tuesday': (ASSIGNMENT_START.date() + (ASSIGNMENT_START.weekday() - ASSIGNMENT_START.weekday())).isoformat(),
        'wednesday': (ASSIGNMENT_START.date() + (2)).isoformat(),
        'thursday': (ASSIGNMENT_START.date() + (3)).isoformat(),
        'friday': (ASSIGNMENT_START.date() + (4)).isoformat(),
        'weds': (ASSIGNMENT_START.date() + 2).isoformat(),
        'wed': (ASSIGNMENT_START.date() + 2).isoformat(),
        'eod': ASSIGNMENT_END.date().isoformat(),
        'evening': ASSIGNMENT_END.date().isoformat(),
        'today': ASSIGNMENT_START.date().isoformat(),
        'tomorrow': (ASSIGNMENT_START.date() + 1).isoformat(),
        'morning': ASSIGNMENT_START.date().isoformat()
    }
    return mapping.get(t)
