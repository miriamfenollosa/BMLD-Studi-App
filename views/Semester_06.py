import streamlit as st
import pandas as pd
from functions.schnittrechner_01 import (
    berechne_schnitt,
    berechne_bereichsschnitt,
    prüfe_praktikum
)

st.title("📚 6. Semester (27 ECTS)")

module_data = [
        {"Bereich": "Gesundheitssystem", "Modul": "Klinische Pharmakologie und personalisierte Medizin", "ECTS": 4},
        {"Bereich": "Gesundheitssystem", "Modul": "Gesundheitssystem und Digital Health", "ECTS": 2},

        {"Bereich": "Kommunikation und Management 2", "Modul": "Projekt-, Change- und Risikomanagement 2", "ECTS": 2},
        {"Bereich": "Kommunikation und Management 2", "Modul": "Forschungsmethoden 2", "ECTS": 2},
        {"Bereich": "Kommunikation und Management 2", "Modul": "Kommunikation 2", "ECTS": 2},
        {"Bereich": "Bachelorarbeit", "Modul": "Bachelorarbeit", "ECTS": 15},
    ]

# Session State
if "df_sem6" not in st.session_state:
    df = pd.DataFrame(module_data)
    df["Note"] = None
    df["Bestanden"] = None
    st.session_state.df_sem6 = df

df = st.session_state.df_sem6

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
            key=f"{bereich}_sem6"
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
            key=f"{bereich}_sem6"
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