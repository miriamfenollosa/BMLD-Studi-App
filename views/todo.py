import streamlit as st
import pandas as pd
from datetime import date

from functions.todo import add_todo, remove_done

st.title("To-Do Liste 📝")

# ---------------------------
# SESSION STATE (WICHTIG)
# ---------------------------
if "todo_df" not in st.session_state:
    st.session_state.todo_df = pd.DataFrame({
        "Fälligkeit": pd.Series(dtype="datetime64[ns]"),
        "Eintrag": pd.Series(dtype="str"),
        "Erledigt": pd.Series(dtype="bool")
    })

# ---------------------------
# EINGABE
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Fälligkeit", value=date.today())

with col2:
    entry = st.text_input("Eintrag")

if st.button("➕ Eintrag hinzufügen"):
    if entry:
        st.session_state.todo_df = add_todo(
            st.session_state.todo_df,
            selected_date,
            entry
        )
        st.success("Eintrag gespeichert!")
        st.rerun()

st.markdown("---")

# ---------------------------
# DATA CLEANING (KRITISCH!)
# ---------------------------
df = st.session_state.todo_df.copy()

df["Erledigt"] = df["Erledigt"].fillna(False).astype(bool)
df["Eintrag"] = df["Eintrag"].fillna("").astype(str)
df["Fälligkeit"] = pd.to_datetime(df["Fälligkeit"], errors="coerce")

# ---------------------------
# ANZEIGE
# ---------------------------
st.subheader("🗂️ Deine Einträge")

edited_df = st.data_editor(
    df,
    column_config={
        "Erledigt": st.column_config.CheckboxColumn("Erledigt"),
        "Fälligkeit": st.column_config.DateColumn(disabled=True),
        "Eintrag": st.column_config.TextColumn(disabled=True),
    },
    use_container_width=True,
    hide_index=True
)

st.session_state.todo_df = edited_df

# ---------------------------
# BUTTONS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Alle Einträge löschen"):
        st.session_state.todo_df = pd.DataFrame({
            "Fälligkeit": pd.Series(dtype="datetime64[ns]"),
            "Eintrag": pd.Series(dtype="str"),
            "Erledigt": pd.Series(dtype="bool")
        })
        st.rerun()

with col2:
    if st.button("☑️ Erledigte löschen"):
        st.session_state.todo_df = remove_done(st.session_state.todo_df)
        st.rerun()
