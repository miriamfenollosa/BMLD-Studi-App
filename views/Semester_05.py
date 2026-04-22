import streamlit as st
import pandas as pd
 
st.title("📚 1. Semester (30 ECTS)")
 
 
module_data = [

    # Wissenschaftliche Grundlagen 1

    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Biologie 1", "ECTS": 5},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Chemie 1", "ECTS": 3},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Informatik 1", "ECTS": 2},
    {"Bereich": "Wissenschaftliche Grundlagen 1", "Modul": "Mathematik 1", "ECTS": 3},
 
    # Basiswissen BMLD 1

    {"Bereich": "Basiswissen BMLD 1", "Modul": "Hämatologie und Hämostaseologie 1", "ECTS": 2},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Medizinische Mikrobiologie 1", "ECTS": 3},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Systemerkrankungen", "ECTS": 3},
    {"Bereich": "Basiswissen BMLD 1", "Modul": "Gesundheitsdaten", "ECTS": 2},
 
    # Grundlagenpraktikum

    {"Bereich": "Praktikum", "Modul": "Grundlagenpraktikum 1", "ECTS": 3},
 
    # Sprache

    {"Bereich": "Sprache", "Modul": "Englisch 1", "ECTS": 2},
    {"Bereich": "Sprache", "Modul": "GLS 1", "ECTS": 2},

]
 
# Session State

if "df" not in st.session_state:

    df = pd.DataFrame(module_data)

    df["Note"] = None

    st.session_state.df = df
 
df = st.session_state.df
 
# ---------------------------

# Anzeige nach Bereichen

# ---------------------------
 
bereiche = df["Bereich"].unique()
 
edited_dfs = []
 
for bereich in bereiche:

    st.subheader(bereich)
 
    teil_df = df[df["Bereich"] == bereich]
 
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

        },

        hide_index=True,

        key=bereich

    )
 
    edited_dfs.append(edited)
 
# Alle Daten wieder zusammenführen

neues_df = pd.concat(edited_dfs).reset_index(drop=True)

st.session_state.df = neues_df
 
# ---------------------------

# Berechnung

# ---------------------------
 
if st.button("📊 Schnitt berechnen"):

    gültig = neues_df.dropna(subset=["Note"])
 
    if len(gültig) == 0:

        st.error("Bitte Noten eingeben.")

    else:

        schnitt = (gültig["Note"] * gültig["ECTS"]).sum() / gültig["ECTS"].sum()
 
        st.success(f"🎓 Dein Semesterschnitt: {schnitt:.2f}")


 