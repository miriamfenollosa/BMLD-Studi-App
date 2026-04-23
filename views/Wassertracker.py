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

    st.session_state.goal = 2.0  # Standardziel
 
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

# CSS für klickbare Boxen

# ---------------------------

st.markdown("""
<style>

div.stButton > button {

    width: 70px;

    height: 90px;

    border-radius: 10px;

    border: 2px solid black;

    margin: 5px;

    font-size: 0px;

    cursor: pointer;

}
</style>

""", unsafe_allow_html=True)
 
# ---------------------------

# Boxen anzeigen (2 Reihen)

# ---------------------------

cols = st.columns(4)
 
for i in range(4):

    with cols[i]:

        color = "#4da6ff" if today_data[i] else "white"

        st.markdown(f"""
<style>

        div[data-testid="stButton"]:has(button[key="top_{i}"]) button {{

            background-color: {color};

        }}
</style>

        """, unsafe_allow_html=True)
 
        if st.button("", key=f"top_{i}"):

            st.session_state.history[today] = toggle_glass(today_data, i)

            st.rerun()
 
cols2 = st.columns(4)
 
for i in range(4, 8):

    with cols2[i - 4]:

        color = "#4da6ff" if today_data[i] else "white"

        st.markdown(f"""
<style>

        div[data-testid="stButton"]:has(button[key="bottom_{i}"]) button {{

            background-color: {color};

        }}
</style>

        """, unsafe_allow_html=True)
 
        if st.button("", key=f"bottom_{i}"):

            st.session_state.history[today] = toggle_glass(today_data, i)

            st.rerun()
 
# ---------------------------

# Berechnung & Zielanzeige

# ---------------------------

total = calculate_water(today_data)
 
st.markdown(f"### 💧 Getrunken: {total:.2f} L")
 
if total >= goal:

    st.success(f"🎯 Ziel erreicht! ({goal:.2f} L)")

else:

    st.info(f"Ziel: {goal:.2f} L")
 