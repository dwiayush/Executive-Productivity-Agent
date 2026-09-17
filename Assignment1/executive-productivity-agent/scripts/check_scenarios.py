from src.pipeline import build_tasks


def run_checks():
    tasks = build_tasks()
    # Vendor list deduplication: look for vendor list text
    vendor_tasks = [t for t in tasks if 'vendor list' in t['title'].lower()]
    print('Vendor list tasks count:', len(vendor_tasks))

    q3 = [t for t in tasks if 'q3 campaign' in t['title'].lower() or any('q3' in s.lower() for s in t.get('sources', []))]
    print('Q3 task found:', q3[0]['deadline'] if q3 else None)

    meridian = [t for t in tasks if 'meridian' in t['title'].lower()]
    print('Meridian owner:', meridian[0]['owner'] if meridian else None, 'deadline:', meridian[0]['deadline'] if meridian else None)

    expense = [t for t in tasks if 'expense variance' in t['title'].lower()]
    print('Expense status:', expense[0]['status'] if expense else None)

    mumbai = [t for t in tasks if 'mumbai' in t['title'].lower()]
    print('Mumbai owner is None?', mumbai and mumbai[0]['owner'] is None)

    # show tasks
    print('\nAll tasks:')
    for t in tasks:
        print('-', t['id'], '|', t['title'], '| owner=', t['owner'], '| deadline=', t.get('deadline'), '| status=', t.get('status'))

    # Q&A checks
    from src.qa_agent import answer_question
    print('\nQ&A: What did I promise Raghav?')
    print(answer_question('What did I promise Raghav?', tasks))
    print('\nQ&A: What needs action today?')
    print(answer_question('What needs action today?', tasks))
    print('\nQ&A: Who owns the Mumbai office lease renewal?')
    print(answer_question('Who owns the Mumbai office lease renewal?', tasks))


if __name__ == '__main__':
    run_checks()
