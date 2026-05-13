import streamlit as st
from datetime import datetime
from functions.Kalender import *
from utils.data_manager import DataManager

st.title("Kalender 📅")


data_manager = DataManager()

if "current_month" not in st.session_state:
    st.session_state.current_month = get_current_month()

if "events" not in st.session_state:
    st.session_state.events = data_manager.load_user_data(
        'calendar_events.json',
        initial_value={}
    )

if "selected_day" not in st.session_state:
    st.session_state.selected_day = None
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

current = st.session_state.current_month
today = datetime.today().strftime("%Y-%m-%d")

st.markdown("""
<style>
.day-box {
    border-radius: 15px;
    padding: 8px;
    height: 110px;
    background-color: #f5f5f7;
    margin-bottom: 6px;
}
.event {
    background-color: #4da6ff;
    color: white;
    border-radius: 8px;
    padding: 2px 6px;
    margin-top: 3px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col1:
    if st.button("←"):
        st.session_state.current_month = prev_month(current)
with col2:
    st.subheader(current.strftime("%B %Y"))
with col3:
    if st.button("→"):
        st.session_state.current_month = next_month(current)

days_header = ["Mo","Di","Mi","Do","Fr","Sa","So"]
cols = st.columns(7)

for i, d in enumerate(days_header):
    cols[i].markdown(f"**{d}**")

days = generate_calendar_days(current)

for week in range(6):
    cols = st.columns(7)

    for i in range(7):
        day = days[week * 7 + i]
        date_str = day.strftime("%Y-%m-%d")

        with cols[i]:
            if day.month != current.month:
                st.markdown("")
                continue
            classes = "day-box"
            if date_str == today:
                classes += " today"
            st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
            st.markdown(f"**{day.day}**")

            if date_str in st.session_state.events:
                for ev in st.session_state.events[date_str]:
                    st.markdown(
                        f"<div class='event'>{ev['start']} - {ev['end']}<br>{ev['text']}</div>",
                        unsafe_allow_html=True
                    )

            st.markdown("</div>", unsafe_allow_html=True)

            if st.button(" ", key=f"day_{date_str}"):
                st.session_state.selected_day = date_str
                st.session_state.edit_index = None

if st.session_state.selected_day:
    st.markdown("---")
    date_str = st.session_state.selected_day
    st.subheader(f"📌 {date_str}")

    events = st.session_state.events.get(date_str, [])

    if events:
        for idx, ev in enumerate(events):
            st.markdown(f"**{ev['text']}** ({ev['start']} - {ev['end']})")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Bearbeiten", key=f"edit_{date_str}_{idx}"):
                    st.session_state.edit_index = idx
            with col2:
                if st.button("Löschen", key=f"del_{date_str}_{idx}"):
                    events.pop(idx)
                    st.session_state.events[date_str] = events
                    # Persist to file
                    data_manager.save_user_data(st.session_state.events, 'calendar_events.json')
                    st.rerun()

    st.markdown("---")

    if st.session_state.edit_index is not None:
        edit_event = events[st.session_state.edit_index]
        st.subheader("🔧 Termin bearbeiten")
        text = st.text_input("Titel", value=edit_event['text'])
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Beginn", value=datetime.strptime(edit_event['start'], "%H:%M").time())
        with col2:
            end_time = st.time_input("Ende", value=datetime.strptime(edit_event['end'], "%H:%M").time())
    else:
        st.subheader("Neuer Termin")
        text = st.text_input("Titel")
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.time_input("Beginn")
        with col2:
            end_time = st.time_input("Ende")

    if st.button("Speichern"):
        if start_time >= end_time:
            st.error("Endzeit muss nach der Startzeit liegen!")
        else:
            new_event = {
                "text": text,
                "start": start_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M"),
            }
            if date_str not in st.session_state.events:
                st.session_state.events[date_str] = []

            if st.session_state.edit_index is not None:
                st.session_state.events[date_str][st.session_state.edit_index] = new_event
                st.session_state.edit_index = None
            else:
                st.session_state.events[date_str].append(new_event)

            data_manager.save_user_data(st.session_state.events, 'calendar_events.json')
            st.success("Termin gespeichert!")
            st.rerun()

