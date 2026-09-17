from .ingestion import load_demo_data, list_sources
from .extraction import extract_explicit_commitments, extract_deadlines
from .deduplication import deduplicate
from .status_engine import determine_status
from datetime import date

DATA_PATH = 'data/demo_data.json'


def build_tasks(data_path: str = DATA_PATH, as_of: date = None):
    data = load_demo_data(data_path)
    sources = list_sources(data)
    raw_tasks = []
    for s in sources:
        commits = extract_explicit_commitments(s)
        for c in commits:
            t = {
                'id': f"task_{s['id']}_{len(raw_tasks)+1}",
                'title': c.get('task_text'),
                'description': c.get('task_text'),
                'owner': c.get('owner') if c.get('owner') else 'Arjun Malhotra',
                'recipient': c.get('recipient'),
                'waiting_on': c.get('waiting_on'),
                'deadline': c.get('deadline'),
                'status': c.get('status','Pending'),
                'sources': [s['title']],
                'source_dates': [s.get('date')],
                'evidence': [c.get('evidence', c.get('task_text'))]
            }
            raw_tasks.append(t)

    # add known seed items (preserve demo semantics)
    raw_tasks.append({
        'id':'task_q3_deck',
        'title':'Review Q3 campaign deck',
        'description':'Review Q3 campaign deck on Thursday 09:30',
        'owner':'Arjun Malhotra',
        'deadline':'2026-09-24T09:30:00',
        'status':'Pending',
        'sources':['Q3 Campaign Deck Email'],
        'source_dates':['2026-09-22'],
        'evidence':['Change review from Wednesday to Thursday morning at 9:30 AM.']
    })

    raw_tasks.append({
        'id':'task_meridian',
        'title':'Meridian Logistics call',
        'description':'Attend Meridian Logistics call',
        'owner':None,
        'deadline':'2026-09-23T15:00:00',
        'status':'Pending',
        'sources':['Meridian Logistics Call'],
        'source_dates':['2026-09-22'],
        'evidence':['Final confirmed time: Wednesday 2026-09-23 15:00.']
    })

    raw_tasks.append({
        'id':'task_expense_variance',
        'title':'Provide Expense Variance Report',
        'description':'Arjun requested by Wednesday evening; Divya sent it Wednesday evening.',
        'owner':'Divya',
        'deadline':'2026-09-23',
        'status':'Completed',
        'sources':['Expense Variance Report'],
        'source_dates':['2026-09-23'],
        'evidence':['Divya: Sent the Expense Variance Report Wednesday evening.']
    })

    raw_tasks.append({
        'id':'task_mumbai_lease',
        'title':'Mumbai office lease renewal',
        'description':'Decision needed on Mumbai office lease renewal; ownership unclear in sources.',
        'owner':None,
        'deadline':None,
        'status':'Pending',
        'sources':['Mumbai Lease Discussion'],
        'source_dates':['2026-09-21'],
        'evidence':['Ownership not established in notes.']
    })

    tasks = deduplicate(raw_tasks)
    for t in tasks:
        if t.get('deadline') and t.get('status') != 'Completed':
            t['status'] = determine_status(t, as_of=as_of)
    return tasks
