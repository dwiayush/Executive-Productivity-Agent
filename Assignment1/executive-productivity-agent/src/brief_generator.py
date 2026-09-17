from datetime import date


def generate_daily_brief(tasks: list, as_of: date):
    brief = {
        'needs_attention': [],
        'my_actions': [],
        'waiting_on_others': [],
        'unclear_ownership': [],
        'upcoming_deadlines': [],
        'due_today': [],
        'completed': []
    }
    for t in tasks:
        status = t.get('status')
        owner = t.get('owner')
        if status == 'Overdue':
            brief['needs_attention'].append(t)
        if owner and owner.lower().startswith('arjun'):
            brief['my_actions'].append(t)
        if t.get('waiting_on') and t.get('waiting_on') != 'Arjun Malhotra':
            brief['waiting_on_others'].append(t)
        if t.get('owner') is None:
            brief['unclear_ownership'].append(t)
        if status == 'Upcoming':
            brief['upcoming_deadlines'].append(t)
        # due today
        dl = t.get('deadline')
        if dl:
            try:
                from .deadline_engine import parse_iso
                d = parse_iso(dl)
                if d and as_of and d == as_of:
                    brief['due_today'].append(t)
            except Exception:
                pass
        if status == 'Completed':
            brief['completed'].append(t)
    return brief
