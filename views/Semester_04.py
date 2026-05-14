import streamlit as st
import pandas as pd
from functions.schnittrechner_01 import (
    berechne_schnitt,
    berechne_bereichsschnitt,
    prüfe_praktikum
)
from utils.data_manager import DataManager

st.title("4. Semester (32 ECTS) 📚")

data_manager = DataManager()

if "show_sem4_result" not in st.session_state:
    st.session_state.show_sem4_result = False

module_data = [
    {"Bereich": "Analyseprozesse und Labordiagnostik 3", "Modul": "Immunhämatologie und Transfusionsmedizin 2", "ECTS": 2},
    {"Bereich": "Analyseprozesse und Labordiagnostik 3", "Modul": "Medizinische Genetik 1", "ECTS": 2},
    {"Bereich": "Analyseprozesse und Labordiagnostik 3", "Modul": "Bewegungsapparat und neurologische Erkrankungen", "ECTS": 3},
    {"Bereich": "Analyseprozesse und Labordiagnostik 3", "Modul": "Endokrinologie, Stoffwechselerkrankungen", "ECTS": 3},
    {"Bereich": "Praktikum", "Modul": "Externes Praktikum Fachbereich I", "ECTS": 11},
    {"Bereich": "Praktikum", "Modul": "Externes Praktikum Fachbereich II", "ECTS": 9},
    {"Bereich": "Praktikum", "Modul": "Praxisreflexion und interprofessionelles Handeln", "ECTS": 2},
]

if "df_sem4" not in st.session_state:
    default_df = pd.DataFrame(module_data)
    default_df["Note"] = None
    default_df["Bestanden"] = None

    loaded_df = data_manager.load_user_data(
        'semester_04_grades.csv',
        initial_value=default_df
    )

    loaded_df["Note"] = pd.to_numeric(loaded_df["Note"], errors="coerce")

    if "Bestanden" in loaded_df.columns:
        loaded_df["Bestanden"] = loaded_df["Bestanden"].apply(
            lambda x: True if str(x).lower() == "true"
            else (False if str(x).lower() == "false" else (x if pd.isna(x) else x))
        )
    else:
        loaded_df["Bestanden"] = pd.NA

    st.session_state.df_sem4 = loaded_df

df = st.session_state.df_sem4

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
            key=f"{bereich}_sem4"
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
            key=f"{bereich}_sem4"
        )

        schnitt_bereich = berechne_bereichsschnitt(edited, bereich)
        if schnitt_bereich is not None:
            st.info(f"📊 Schnitt {bereich}: {schnitt_bereich:.2f}")
        else:
            st.info(f"📊 Schnitt {bereich}: keine Noten")

    edited_dfs.append(edited)

neues_df = pd.concat(edited_dfs).reset_index(drop=True)
st.session_state.df_sem4 = neues_df

data_manager.save_user_data(st.session_state.df_sem4, 'semester_04_grades.csv')

st.markdown("---")

if st.button("📊 Semesterschnitt berechnen"):
    st.session_state.show_sem4_result = True

if st.session_state.show_sem4_result:

    ohne_praktikum = neues_df[neues_df["Bereich"] != "Praktikum"]
    schnitt = berechne_schnitt(ohne_praktikum)

    if schnitt is None:
        st.error("Bitte Noten eingeben.")
    else:
        st.success(f"Semesterschnitt: {schnitt:.2f}")

    praktika_df = neues_df[neues_df["Bereich"] == "Praktikum"].copy()

    praktika_df["Bestanden_status"] = praktika_df["Bestanden"].apply(
        lambda x: "unknown" if pd.isna(x) else ("passed" if bool(x) else "failed")
    )

    num = len(praktika_df)
    num_pass = (praktika_df["Bestanden_status"] == "passed").sum()
    num_fail = (praktika_df["Bestanden_status"] == "failed").sum()
    num_unknown = (praktika_df["Bestanden_status"] == "unknown").sum()

    if num > 0 and num_pass == num and num_unknown == 0:
        st.success("Alle Praktika bestanden!")

    elif num > 0 and num_fail == num and num_unknown == 0:
        st.error("Alle Praktika nicht bestanden!")

    else:
        for _, row in praktika_df.iterrows():
            modul = row["Modul"]
            status = row["Bestanden_status"]

            if status == "passed":
                st.success(f"{modul}: Bestanden")
            elif status == "failed":
                st.error(f"{modul}: Nicht bestanden")
            else:
                st.warning(f"{modul}: Noch nicht bewertet")