import streamlit as st
from functions.Wassertracker import (
    get_today,
    init_day,
    toggle_glass,
    calculate_water
)
 
st.title("💧 Wasser-Trink-Tracker")
 
st.write("1 Glas = 0.25L")
 
# ---------------------------
# Session State
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = {}
 
history = st.session_state.history
 
# aktuelles Datum
today = get_today()
 
# neuen Tag initialisieren
history = init_day(history)
st.session_state.history = history
 
# Datum anzeigen
st.subheader(f"📅 Heute: {today}")
 
today_data = history[today]
 
# ---------------------------
# CSS für farbige Boxen
# ---------------------------
st.markdown("""
<style>
.box {
    width: 60px;
    height: 80px;
    border: 2px solid black;
    border-radius: 8px;
    margin: 5px auto;
}
.blue {
    background-color: #4da6ff;
}
.white {
    background-color: white;
}
</style>
""", unsafe_allow_html=True)
 
# ---------------------------
# Boxen anzeigen (2 Reihen)
# ---------------------------
cols = st.columns(4)
 
for i in range(4):
    with cols[i]:
        color = "blue" if today_data[i] else "white"
 
        if st.button(" ", key=f"top_{i}"):
            st.session_state.history[today] = toggle_glass(today_data, i)
            st.rerun()
 
        st.markdown(f'<div class="box {color}"></div>', unsafe_allow_html=True)
 
cols2 = st.columns(4)
 
for i in range(4, 8):
    with cols2[i - 4]:
        color = "blue" if today_data[i] else "white"
 
        if st.button(" ", key=f"bottom_{i}"):
            st.session_state.history[today] = toggle_glass(today_data, i)
            st.rerun()
 
        st.markdown(f'<div class="box {color}"></div>', unsafe_allow_html=True)
 
# ---------------------------
# Berechnung
# ---------------------------
total = calculate_water(today_data)
 
st.markdown(f"### 💧 Getrunken: {total:.2f} L")
 
goal = 2.0
 
if total >= goal:
    st.success("🎯 Ziel erreicht!")
else:
    st.info(f"Ziel: {goal} L")