import streamlit as st
import pandas as pd
from datetime import date

st.title("📅 Kalender")

# Session State
if "calendar_df" not in st.session_state:
    st.session_state.calendar_df = pd.DataFrame({
        "Datum": [],
        "Eintrag": []
    })

df = st.session_state.calendar_df

# Eingabe
col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Datum", value=date.today())

with col2:
    entry = st.text_input("Eintrag")

if st.button("➕ Eintrag hinzufügen"):
    if entry:
        new_row = {"Datum": selected_date, "Eintrag": entry}
        st.session_state.calendar_df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Eintrag gespeichert!")

st.markdown("---")

# Anzeige
st.subheader("🗂️ Deine Einträge")

st.dataframe(st.session_state.calendar_df, use_container_width=True)

# Optional: löschen
if st.button("🧹 Alle Einträge löschen"):
    st.session_state.calendar_df = pd.DataFrame(columns=["Datum", "Eintrag"])
