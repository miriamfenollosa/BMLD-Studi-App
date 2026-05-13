import streamlit as st
from functions.Wassertracker import (
    get_today,
    init_day,
    toggle_glass,
    calculate_water
)
from utils.data_manager import DataManager

st.title("Wassertracker 💧")
st.write("1 Glas = 0.25L")

data_manager = DataManager()

if "history" not in st.session_state:
    st.session_state.history = data_manager.load_user_data(
        'water_tracker.json',
        initial_value={}
    )

if "goal" not in st.session_state:
    st.session_state.goal = 2.0

history = st.session_state.history

today = get_today()

GLASS_SIZE = 0.25
num_glasses = int(st.session_state.goal / GLASS_SIZE)
num_glasses = max(1, min(num_glasses, 20))

history = init_day(history, num_glasses)
st.session_state.history = history

today_data = history[today]

if len(today_data) != num_glasses:
    today_data = [False] * num_glasses
    history[today] = today_data
    st.session_state.history = history
    data_manager.save_user_data(st.session_state.history, 'water_tracker.json')

st.subheader(f"Heute: {today}")

with st.expander("Zielmengenrechner"):
    gewicht = st.number_input(
        "Dein Körpergewicht (kg):",
        min_value=10.0,
        max_value=300.0,
        step=0.5,
        value=70.0
    )

    empfehlung = gewicht * 0.035
    st.write(f"Empfohlene Tagesmenge: **{empfehlung:.2f} L**")

    if st.button("Als Ziel übernehmen"):
        st.session_state.goal = empfehlung
        num_glasses_new = int(empfehlung / GLASS_SIZE)
        num_glasses_new = max(1, min(num_glasses_new, 20))
        history[today] = [False] * num_glasses_new
        st.session_state.history = history

        data_manager.save_user_data(st.session_state.history, 'water_tracker.json')
        st.success(f"✅ Ziel auf {empfehlung:.2f} L gesetzt!")
        st.rerun()

goal = st.session_state.goal

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

st.subheader(f"Deine Gläser ({num_glasses})")

cols = st.columns(4)

for i in range(num_glasses):
    col = cols[i % 4]
    with col:
        icon = "💧" if today_data[i] else" "
        if st.button(icon, key=f"glass_{i}"):
            st.session_state.history[today] = toggle_glass(today_data, i)
            data_manager.save_user_data(st.session_state.history, 'water_tracker.json')
            st.rerun()

total = calculate_water(today_data)

st.markdown(f"###  Getrunken: {total:.2f} L")

if total >= goal:
    st.success(f"🎯 Ziel erreicht! ({goal:.2f} L)")
else:
    st.info(f"Ziel: {goal:.2f} L ({num_glasses} Gläser)")
