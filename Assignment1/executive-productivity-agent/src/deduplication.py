from difflib import SequenceMatcher
from dateutil import parser


def normalize_text(s: str):
    return ' '.join(s.lower().strip().split())


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def deduplicate(tasks: list, threshold: float = 0.75):
    unique = []
    # domain keywords to force-merge related items
    context_keywords = ['vendor list', 'vendor', 'q3 campaign', 'expense variance', 'mumbai', 'meridian']
    for t in tasks:
        nt = normalize_text(t['title'])
        merged = False
        for u in unique:
            # if titles share a context keyword, treat as duplicate
            t_keys = [kw for kw in context_keywords if kw in nt]
            u_keys = [kw for kw in context_keywords if kw in normalize_text(u['title'])]
            share_key = bool(set(t_keys) & set(u_keys))
            if share_key or similar(nt, normalize_text(u['title'])) >= threshold:
                # merge sources
                # ensure sources are lists
                if not isinstance(u.get('sources'), list):
                    u['sources'] = [u.get('sources')] if u.get('sources') else []
                u['sources'].extend(t.get('sources', []))
                # ensure evidence is a list
                if not isinstance(u.get('evidence'), list):
                    u['evidence'] = [u.get('evidence')] if u.get('evidence') else []
                # append or extend evidence depending on type
                tev = t.get('evidence', '')
                if isinstance(tev, list):
                    # flatten any nested lists and ensure strings
                    flat = []
                    for x in tev:
                        if isinstance(x, list):
                            flat.extend([str(i) for i in x])
                        else:
                            flat.append(str(x))
                    u['evidence'].extend(flat)
                else:
                    u['evidence'].append(str(tev))
                # prefer newer/non-None fields from t when present
                # merge source_dates
                if not isinstance(u.get('source_dates'), list):
                    u['source_dates'] = [u.get('source_dates')] if u.get('source_dates') else []
                u['source_dates'].extend(t.get('source_dates', []))
                # prefer fields from the task with the latest source date
                def latest_val(u, t, key):
                    try:
                        u_dates = [parser.parse(d).date() for d in (u.get('source_dates') or []) if d]
                        t_dates = [parser.parse(d).date() for d in (t.get('source_dates') or []) if d]
                        u_max = max(u_dates) if u_dates else None
                        t_max = max(t_dates) if t_dates else None
                        if t_max and (not u_max or t_max >= u_max):
                            return t.get(key)
                        return u.get(key)
                    except Exception:
                        return t.get(key) or u.get(key)

                u['owner'] = latest_val(u, t, 'owner')
                u['deadline'] = latest_val(u, t, 'deadline')
                # update status: prefer Completed, else latest
                if (t.get('status') == 'Completed') or (u.get('status') == 'Completed'):
                    u['status'] = 'Completed'
                else:
                    u['status'] = latest_val(u, t, 'status')
                merged = True
                break
        if not merged:
            # normalize sources/evidence to lists
            tt = t.copy()
            if not isinstance(tt.get('sources'), list):
                tt['sources'] = [tt.get('sources')] if tt.get('sources') else []
            if not isinstance(tt.get('evidence'), list):
                tt['evidence'] = [tt.get('evidence')] if tt.get('evidence') else []
            unique.append(tt)
    return unique
