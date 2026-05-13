import streamlit as st
import pandas as pd
from functions.schnittrechner_01 import (
    berechne_schnitt,
    berechne_bereichsschnitt,
    prüfe_praktikum
)
from utils.data_manager import DataManager

st.title("5. Semester (33 ECTS) 📚")

data_manager = DataManager()

module_data = [
    {"Bereich": "Analyseprozesse und Labordiagnostik 4", "Modul": "Medizinische Genetik 2", "ECTS": 2},
    {"Bereich": "Analyseprozesse und Labordiagnostik 4", "Modul": "Urogenitale und gastrointestinale Erkrankungen", "ECTS": 3},
    {"Bereich": "Analyseprozesse und Labordiagnostik 4", "Modul": "Entwicklungsstörungen und vererbbare Erkrankungen", "ECTS": 3},

    {"Bereich": "Kommunikation und Management 1", "Modul": "Projekt-, Change- und Risikomanagement 1", "ECTS": 4},
    {"Bereich": "Kommunikation und Management 1", "Modul": "Kommunikation 1", "ECTS": 4},
    {"Bereich": "Kommunikation und Management 1", "Modul": "Evidenzbasiertes Handeln", "ECTS": 2},
    {"Bereich": "Kommunikation und Management 1", "Modul": "Entwicklungs-, Trend-, Unternehmertum", "ECTS": 2},
    {"Bereich": "Kommunikation und Management 1", "Modul": "Gesundheitsförderung und Prävention", "ECTS": 2},

    {"Bereich": "Angewandte Forschung", "Modul": "Projektarbeit", "ECTS": 6},
    {"Bereich": "Angewandte Forschung", "Modul": "Forschungsmethoden 1", "ECTS": 2},

    {"Bereich": "Gesellschaft, Kultur und Gesundheit", "Modul": "Module gemäß separater Liste", "ECTS": 3},
]

if "df_sem5" not in st.session_state:
    default_df = pd.DataFrame(module_data)
    default_df["Note"] = None
    default_df["Bestanden"] = None
    
    loaded_df = data_manager.load_user_data(
        'semester_05_grades.csv',
        initial_value=default_df
    )
    
    loaded_df["Note"] = pd.to_numeric(loaded_df["Note"], errors="coerce")
    loaded_df["Bestanden"] = loaded_df["Bestanden"].fillna(False).astype(bool)
    
    st.session_state.df_sem5 = loaded_df

df = st.session_state.df_sem5

bereiche = df["Bereich"].unique()
edited_dfs = []

for bereich in bereiche:
    st.subheader(bereich)
    teil_df = df[df["Bereich"] == bereich]
    if bereich == "Praktikum":
        edited = st.data_editor(
            teil_df,
            column_config={
                "Modul": st.column_config.TextColumn(disabled=True),
                "ECTS": st.column_config.NumberColumn(disabled=True),
                "Bestanden": st.column_config.CheckboxColumn("Bestanden"),
                "Note": None,
            },
            hide_index=True,
            key=f"{bereich}_sem5"
        )
    else:
        edited = st.data_editor(
            teil_df,
            column_config={
                "Modul": st.column_config.TextColumn(disabled=True),
                "ECTS": st.column_config.NumberColumn(disabled=True),
                "Note": st.column_config.NumberColumn(
                    min_value=1.0,
                    max_value=6.0,
                    step=0.25
                ),
                "Bestanden": None,
            },
            hide_index=True,
            key=f"{bereich}_sem5"
        )

        schnitt_bereich = berechne_bereichsschnitt(edited, bereich)

        if schnitt_bereich is not None:
            st.info(f"📊 Schnitt {bereich}: {schnitt_bereich:.2f}")
        else:
            st.info(f"📊 Schnitt {bereich}: keine Noten")

    edited_dfs.append(edited)

neues_df = pd.concat(edited_dfs).reset_index(drop=True)
st.session_state.df_sem5 = neues_df

data_manager.save_user_data(st.session_state.df_sem5, 'semester_05_grades.csv')

st.markdown("---")

if st.button("📊 Semesterschnitt berechnen"):

    ohne_praktikum = neues_df[neues_df["Bereich"] != "Praktikum"]
    schnitt = berechne_schnitt(ohne_praktikum)
    if schnitt is None:
        st.error("Bitte Noten eingeben.")
    else:
        st.success(f"Semesterschnitt: {schnitt:.2f}")
        status = prüfe_praktikum(neues_df)