import streamlit as st
from datetime import date
import os
from src.pipeline import build_tasks
from src.brief_generator import generate_daily_brief
from src.qa_agent import answer_question
from src.ingestion import load_demo_data

st.set_page_config(page_title='Executive Productivity Agent', layout='wide')

# Header / top bar
col1, col2 = st.columns([3,1])
with col1:
    st.title('Executive Productivity Agent')
    st.markdown('**Arjun Malhotra — VP Sales**')
with col2:
    # AI Mode indicator
    OPENAI = bool(os.getenv('OPENAI_API_KEY'))
    if OPENAI:
        st.success('AI Mode: OpenAI')
    else:
        st.info('AI Mode: Deterministic Demo')

# Sidebar: demo date control
st.sidebar.header('Demo Controls')
demo_date = st.sidebar.selectbox('Assignment Date', [
    date(2026,9,21),
    date(2026,9,22),
    date(2026,9,23),
    date(2026,9,24),
    date(2026,9,25)
], index=0)

st.sidebar.markdown('Assignment Week: 21 — 25 Sep 2026')

# Build tasks relative to selected demo date
tasks = build_tasks(as_of=demo_date)
brief = generate_daily_brief(tasks, demo_date)

main, right = st.columns([2,1])

with main:
    st.header('Daily Action Brief')
    st.markdown(f"**What does Arjun need to pay attention to on {demo_date.isoformat()}?**")

    # Priority order
    if brief['needs_attention']:
        st.subheader('🔴 Overdue — Needs Attention')
        for t in brief['needs_attention']:
            with st.expander(t['title']):
                st.write('**Status:**', t.get('status'))
                st.write('**Owner:**', t.get('owner'))
                st.write('**Deadline:**', t.get('deadline'))
                st.write('**Sources:**')
                for s,sd in zip(t.get('sources',[]), t.get('source_dates',[])):
                    st.write('-', s, sd)
                st.write('**Evidence:**')
                for e in t.get('evidence',[]):
                    st.write('-', e)

    if brief.get('due_today'):
        st.subheader('📅 Actions Due Today')
        for t in brief['due_today']:
            with st.expander(t['title']):
                st.write('**Status:**', t.get('status'))
                st.write('**Owner:**', t.get('owner'))
                st.write('**Deadline:**', t.get('deadline'))
                for s,sd in zip(t.get('sources',[]), t.get('source_dates',[])):
                    st.write('-', s, sd)
                st.write('**Evidence:**')
                for e in t.get('evidence',[]):
                    st.write('-', e)

    if brief['unclear_ownership']:
        st.subheader('⚠️ Unclear Ownership')
        for t in brief['unclear_ownership']:
            with st.expander(t['title']):
                st.write('OWNER: ⚠️ Ownership unclear')
                st.write('Ownership could not be established from the provided sources.')
                st.write('**Sources & Evidence:**')
                for s,sd in zip(t.get('sources',[]), t.get('source_dates',[])):
                    st.write('-', s, sd)
                for e in t.get('evidence',[]):
                    st.write('-', e)

    if brief['upcoming_deadlines']:
        st.subheader('⏰ Upcoming Deadlines')
        for t in brief['upcoming_deadlines']:
            with st.expander(t['title']):
                st.write('**Status:**', t.get('status'))
                st.write('**Deadline:**', t.get('deadline'))
                for s,sd in zip(t.get('sources',[]), t.get('source_dates',[])):
                    st.write('-', s, sd)

    if brief['waiting_on_others']:
        st.subheader('⏳ Waiting on Others')
        for t in brief['waiting_on_others']:
            with st.expander(t['title']):
                st.write('**Owner:**', t.get('owner'))
                st.write('**Waiting on:**', t.get('waiting_on'))
                for s,sd in zip(t.get('sources',[]), t.get('source_dates',[])):
                    st.write('-', s, sd)

    st.subheader('✅ Completed / Resolved')
    for t in brief['completed']:
        st.write('-', t['title'])

    st.markdown('---')
    st.header('Sources / Evidence')
    _data = load_demo_data('data/demo_data.json')
    for s in _data.get('sources', []):
        with st.expander(f"{s['title']} — {s.get('date','')}"):
            st.write(s.get('content',''))

with right:
    st.header('Quick Q&A')
    q = st.text_input('Ask a question grounded in the Data Pack')
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button('What did I promise Raghav?'):
            q = 'What did I promise Raghav?'
    with col_b:
        if st.button('What needs action today?'):
            q = 'What needs action today?'
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button('What am I waiting on?'):
            q = 'What am I waiting on?'
    with col_d:
        if st.button('Who owns the Mumbai office lease renewal?'):
            q = 'Who owns the Mumbai office lease renewal?'

    if st.button('Ask'):
        if q.strip() == '':
            st.info('Please enter a question or use an example button.')
        else:
            res = answer_question(q, tasks)
            if isinstance(res, dict) and res.get('answer'):
                st.subheader('Answer')
                st.write(res['answer'])
                st.subheader('Supporting evidence')
                for sid in res.get('sources', []):
                    # find source task
                    for t in tasks:
                        if t.get('id') == sid:
                            for e in t.get('evidence', []):
                                st.write('-', e)
                st.subheader('Sources')
                st.write(res.get('sources', []))
            else:
                # deterministic list
                st.subheader('Results')
                for t in (res if isinstance(res, list) else []):
                    st.write('-', t.get('title'))

    st.markdown('---')
    st.header("Today's Calendar")
    today_events = [t for t in tasks if t.get('deadline') and t.get('status') != 'Completed']
    # show items with deadline matching demo_date
    for t in today_events:
        if t.get('deadline') and demo_date.isoformat() in str(t.get('deadline')):
            st.write('-', t.get('deadline'), t.get('title'))
