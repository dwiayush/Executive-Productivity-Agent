import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'data' / 'epa.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        title TEXT,
        owner TEXT,
        recipient TEXT,
        waiting_on TEXT,
        deadline TEXT,
        status TEXT,
        sources TEXT,
        evidence TEXT
    )''')
    conn.commit()
    conn.close()


def save_task(task: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO tasks (id,title,owner,recipient,waiting_on,deadline,status,sources,evidence) VALUES (?,?,?,?,?,?,?,?,?)',
              (task.get('id'), task.get('title'), task.get('owner'), task.get('recipient'), task.get('waiting_on'), task.get('deadline'), task.get('status'), '\n'.join(task.get('sources',[])), task.get('evidence','')))
    conn.commit()
    conn.close()
