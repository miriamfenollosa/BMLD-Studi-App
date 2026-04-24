import streamlit as st
import pandas as pd
from datetime import date

from functions.todo import add_todo, remove_done

st.title("To-Do Liste 📝")

# SESSION STATE
if "todo_df" not in st.session_state:
    st.session_state.todo_df = pd.DataFrame({
        "Fälligkeit": [],
        "Eintrag": [],
        "Erledigt": []
    })

if "Erledigt" not in st.session_state.todo_df.columns:
    st.session_state.todo_df["Erledigt"] = False

df = st.session_state.todo_df

# EINGABE
col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Fälligkeit", value=date.today())

with col2:
    entry = st.text_input("Eintrag")

if st.button("➕ Eintrag hinzufügen"):
    if entry:
        st.session_state.todo_df = add_todo(df, selected_date, entry)
        st.success("Eintrag gespeichert!")
        st.rerun()

st.markdown("---")

# ANZEIGE
st.subheader("🗂️ Deine Einträge")

edited_df = st.data_editor(
    st.session_state.todo_df,
    column_config={
        "Erledigt": st.column_config.CheckboxColumn("Erledigt"),
        "Fälligkeit": st.column_config.DateColumn(disabled=True),
        "Eintrag": st.column_config.TextColumn(disabled=True),
    },
    use_container_width=True,
    hide_index=True
)

st.session_state.todo_df = edited_df

# FILTER / CLEANUP LOGIK
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Alle Einträge löschen"):
        st.session_state.todo_df = pd.DataFrame(columns=["Fälligkeit", "Eintrag", "Erledigt"])
        st.rerun()

with col2:
    if st.button("☑️ Nur erledigte löschen"):
        st.session_state.todo_df = st.session_state.todo_df[
            st.session_state.todo_df["Erledigt"] == False
        ].reset_index(drop=True)
        st.rerun()
