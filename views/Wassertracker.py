import streamlit as st
from functions.Wassertracker import (
    get_today,
    init_day,
    toggle_glass,
    calculate_water
)

st.title("Wassertracker 💧")
st.write("1 Glas = 0.25L")

# ---------------------------
# Session State
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = {}

if "goal" not in st.session_state:
    st.session_state.goal = 2.0

history = st.session_state.history

today = get_today()

# ---------------------------
# Ziel → Gläser berechnen
# ---------------------------
GLASS_SIZE = 0.25
num_glasses = int(st.session_state.goal / GLASS_SIZE)
num_glasses = max(1, min(num_glasses, 20))  # Sicherheitslimit

# ---------------------------
# neuen Tag initialisieren
# ---------------------------
history = init_day(history, num_glasses)
st.session_state.history = history

today_data = history[today]

# Falls Ziel geändert wurde → Liste anpassen
if len(today_data) != num_glasses:
    today_data = [False] * num_glasses
    history[today] = today_data
    st.session_state.history = history

# ---------------------------
# Datum anzeigen
# ---------------------------
st.subheader(f"📅 Heute: {today}")

# ---------------------------
# Zielmengenrechner
# ---------------------------
with st.expander("⚙️ Zielmengenrechner"):
    gewicht = st.number_input(
        "Dein Körpergewicht (kg):",
        min_value=10.0,
        max_value=300.0,
        step=0.5,
        value=70.0
    )

    empfehlung = gewicht * 0.035
    st.write(f"💡 Empfohlene Tagesmenge: **{empfehlung:.2f} L**")

    if st.button("Als Ziel übernehmen"):
        st.session_state.goal = empfehlung
        st.success(f"✅ Ziel auf {empfehlung:.2f} L gesetzt!")

goal = st.session_state.goal

# ---------------------------
# CSS für Buttons
# ---------------------------
st.markdown("""
<style>
div.stButton > button {
    width: 70px;
    height: 90px;
    border-radius: 10px;
    border: 2px solid #1a1a2e;
    margin: 5px;
    font-size: 24px;
    cursor: pointer;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Wasser-Boxen dynamisch
# ---------------------------
st.subheader(f"💧 Deine Gläser ({num_glasses})")

cols = st.columns(4)

for i in range(num_glasses):
    col = cols[i % 4]
    with col:
        icon = "💧" if today_data[i] else ""
        if st.button(icon, key=f"glass_{i}"):
            st.session_state.history[today] = toggle_glass(today_data, i)
            st.rerun()

# ---------------------------
# Berechnung
# ---------------------------
total = calculate_water(today_data)

st.markdown(f"### 💧 Getrunken: {total:.2f} L")

if total >= goal:
    st.success(f"🎯 Ziel erreicht! ({goal:.2f} L)")
else:
    st.info(f"Ziel: {goal:.2f} L ({num_glasses} Gläser)")
