import streamlit as st
import pandas as pd
from functions.schnittrechner_01 import (
    berechne_schnitt,
    berechne_bereichsschnitt,
    prüfe_praktikum
)
from utils.data_manager import DataManager

st.title("📚 1. Semester (30 ECTS)")

# ---------------------------
# Initialize DataManager
# ---------------------------
data_manager = DataManager()

module_data = [
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Biologie 1", "ECTS": 5},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Chemie 1", "ECTS": 3},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Informatik 1", "ECTS": 2},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Mathematik 1", "ECTS": 3},

    {"Bereich": "Basiswissen BMLD 1", "Modul": "Hämatologie und Hämostaseologie 1", "ECTS": 2},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Medizinische Mikrobiologie 1", "ECTS": 3},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Systemerkrankungen", "ECTS": 3},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Gesundheitsdaten", "ECTS": 2},

    {"Bereich": "Sprache", "Modul": "Englisch 1", "ECTS": 2},
    {"Bereich": "Sprache", "Modul": "GKS 1", "ECTS": 2},

    {"Bereich": "Praktikum", "Modul": "Grundlagenpraktikum 1", "ECTS": 3},
]

# Session State (wichtig: eigener Name!)
if "df_sem1" not in st.session_state:
    # Load grades from persisted file, or create empty DataFrame with module data
    default_df = pd.DataFrame(module_data)
    default_df["Note"] = None
    default_df["Bestanden"] = None
    
    loaded_df = data_manager.load_user_data(
        'semester_01_grades.csv',
        initial_value=default_df
    )
    
    # Clean up data types: convert Note to float, Bestanden to bool, handle NaN
    loaded_df["Note"] = pd.to_numeric(loaded_df["Note"], errors="coerce")
    loaded_df["Bestanden"] = loaded_df["Bestanden"].fillna(False).astype(bool)
    
    st.session_state.df_sem1 = loaded_df

df = st.session_state.df_sem1

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
            key=f"{bereich}_sem1"
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
            key=f"{bereich}_sem1"
        )

        schnitt_bereich = berechne_bereichsschnitt(edited, bereich)

        if schnitt_bereich is not None:
            st.info(f"📊 Schnitt {bereich}: {schnitt_bereich:.2f}")
        else:
            st.info(f"📊 Schnitt {bereich}: keine Noten")

    edited_dfs.append(edited)

# Zusammenführen
neues_df = pd.concat(edited_dfs).reset_index(drop=True)
st.session_state.df_sem1 = neues_df

# Persist grades to file
data_manager.save_user_data(st.session_state.df_sem1, 'semester_01_grades.csv')

st.markdown("---")

# Gesamtberechnung
if st.button("📊 Semesterschnitt berechnen"):

    ohne_praktikum = neues_df[neues_df["Bereich"] != "Praktikum"]
    schnitt = berechne_schnitt(ohne_praktikum)

    if schnitt is None:
        st.error("Bitte Noten eingeben.")
    else:
        st.success(f"🎓 Semesterschnitt: {schnitt:.2f}")

        status = prüfe_praktikum(neues_df)

        if status == "bestanden":
            st.success("✅ Praktikum bestanden")
        elif status == "nicht bestanden":
            st.error("❌ Praktikum nicht bestanden")
        else:
            st.warning("⚠️ Praktikum noch nicht bewertet")
