from datetime import datetime, date
from dateutil import parser

ASSIGNMENT_START = datetime(2026,9,21).date()
ASSIGNMENT_END = datetime(2026,9,25).date()


def parse_iso(date_iso: str):
    if not date_iso:
        return None
    try:
        return parser.parse(date_iso).date()
    except Exception:
        return None


def is_overdue(deadline_iso: str, as_of: date = ASSIGNMENT_END):
    d = parse_iso(deadline_iso)
    if not d:
        return False
    return d < as_of


def is_upcoming(deadline_iso: str, as_of: date = ASSIGNMENT_START):
    d = parse_iso(deadline_iso)
    if not d:
        return False
    # upcoming within assignment week
    return ASSIGNMENT_START <= d <= ASSIGNMENT_END
