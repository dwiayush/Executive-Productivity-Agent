from datetime import date
from .deadline_engine import is_overdue, is_upcoming


def determine_status(task: dict, as_of=None):
    dl = task.get('deadline')
    if dl:
        # preserve original behavior when as_of is None
        if as_of is None:
            if is_overdue(dl):
                return 'Overdue'
            if is_upcoming(dl):
                return 'Upcoming'
            return 'Scheduled'
        else:
            if is_overdue(dl, as_of=as_of):
                return 'Overdue'
            if is_upcoming(dl, as_of=as_of):
                return 'Upcoming'
            return 'Scheduled'
    # no deadline
    return 'Pending'
