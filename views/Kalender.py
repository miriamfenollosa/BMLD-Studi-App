import streamlit as st
from datetime import datetime
from functions.Kalender import *
 
st.title("📅 Kalender")
 
# ---------------------------
# Session State
# ---------------------------
if "current_month" not in st.session_state:
    st.session_state.current_month = get_current_month()
 
if "events" not in st.session_state:
    st.session_state.events = {}
 
current = st.session_state.current_month
today = datetime.today().strftime("%Y-%m-%d")
 
# ---------------------------
# Styling (clean & weich)
# ---------------------------
st.markdown("""
<style>
.day-box {
    border-radius: 15px;
    padding: 8px;
    height: 110px;
    background-color: #f5f5f7;
    margin-bottom: 6px;
}
.today {
    background-color: #d0e7ff;
    border: 2px solid #4da6ff;
}
.other-month {
    opacity: 0.4;
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
 
# ---------------------------
# Navigation
# ---------------------------
col1, col2, col3 = st.columns([1,2,1])
 
with col1:
    if st.button("⬅️"):
        st.session_state.current_month = prev_month(current)
 
with col2:
    st.subheader(current.strftime("%B %Y"))
 
with col3:
    if st.button("➡️"):
        st.session_state.current_month = next_month(current)
 
# ---------------------------
# Wochentage
# ---------------------------
days_header = ["Mo","Di","Mi","Do","Fr","Sa","So"]
cols = st.columns(7)
 
for i, d in enumerate(days_header):
    cols[i].markdown(f"**{d}**")
 
# ---------------------------
# Kalender
# ---------------------------
days = generate_calendar_days(current)
 
for week in range(6):
    cols = st.columns(7)
 
    for i in range(7):
        day = days[week * 7 + i]
        date_str = day.strftime("%Y-%m-%d")
 
        with cols[i]:
            classes = "day-box"
            if date_str == today:
                classes += " today"
            if day.month != current.month:
                classes += " other-month"
 
            st.markdown(f"<div class='{classes}'>", unsafe_allow_html=True)
 
            # Datum anzeigen
            st.markdown(f"**{day.day}**")
 
            # Events anzeigen
            if date_str in st.session_state.events:
                for ev in st.session_state.events[date_str]:
                    st.markdown(
                        f"<div class='event'>{ev['time']} - {ev['text']}</div>",
                        unsafe_allow_html=True
                    )
 
            st.markdown("</div>", unsafe_allow_html=True)
 
            # 👉 KLICK AUF TAG (unsichtbarer Button)
            if st.button("", key=f"day_{date_str}"):
                st.session_state.selected_day = date_str
 
# ---------------------------
# Event direkt eingeben
# ---------------------------
if "selected_day" in st.session_state:
    st.markdown("---")
    st.subheader(f"📌 {st.session_state.selected_day}")
 
    col1, col2 = st.columns(2)
 
    with col1:
        text = st.text_input("Termin")
 
    with col2:
        time = st.time_input("Zeit")
 
    if st.button("Speichern"):
        if st.session_state.selected_day not in st.session_state.events:
            st.session_state.events[st.session_state.selected_day] = []
 
        st.session_state.events[st.session_state.selected_day].append({
            "text": text,
            "time": time.strftime("%H:%M")
        })
 
        st.success("Gespeichert!")
        st.rerun()