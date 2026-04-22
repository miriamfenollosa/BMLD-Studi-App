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
 
    # Praktikum

    {"Bereich": "Praktikum", "Modul": "Grundlagenpraktikum 1", "ECTS": 3},
 
    # Sprache

    {"Bereich": "Sprache", "Modul": "Englisch 1", "ECTS": 2},

    {"Bereich": "Sprache", "Modul": "GLS 1", "ECTS": 2},

]
 
# Session State

if "df" not in st.session_state:

    df = pd.DataFrame(module_data)

    df["Note"] = None

    df["Bestanden"] = None  # NEU

    st.session_state.df = df
 
df = st.session_state.df
 
bereiche = df["Bereich"].unique()

edited_dfs = []
 
for bereich in bereiche:

    st.subheader(bereich)
 
    teil_df = df[df["Bereich"] == bereich]
 
    # 🔥 Unterschied für Praktikum

    if bereich == "Praktikum":

        edited = st.data_editor(

            teil_df,

            column_config={

                "Modul": st.column_config.TextColumn(disabled=True),

                "ECTS": st.column_config.NumberColumn(disabled=True),

                "Bestanden": st.column_config.CheckboxColumn("Bestanden"),

                "Note": None,  # Note wird nicht angezeigt

            },

            hide_index=True,

            key=bereich

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

            key=bereich

        )
 
    edited_dfs.append(edited)
 
# Zusammenführen

neues_df = pd.concat(edited_dfs).reset_index(drop=True)

st.session_state.df = neues_df
 
# ---------------------------

# Berechnung

# ---------------------------
 
if st.button("📊 Schnitt berechnen"):
 
    # 👉 OHNE Praktikum

    ohne_praktikum = neues_df[neues_df["Bereich"] != "Praktikum"]

    gültig = ohne_praktikum.dropna(subset=["Note"])
 
    if len(gültig) == 0:

        st.error("Bitte Noten eingeben.")

    else:

        # 🔢 Semesterschnitt

        schnitt = (gültig["Note"] * gültig["ECTS"]).sum() / gültig["ECTS"].sum()

        st.success(f"🎓 Semesterschnitt: {schnitt:.2f}")
 
        # ⭐ Beste / schlechteste

        st.write(f"⭐ Beste Note: {gültig['Note'].max()}")

        st.write(f"⚠️ Schlechteste Note: {gültig['Note'].min()}")
 
        st.markdown("---")
 
        # 📊 Schnitte pro Bereich

        st.subheader("📊 Schnitte pro Bereich")
 
        for bereich in ["Wissenschaftliche Grundlagen 1", "Basiswissen BMLD 1", "Sprache"]:

            teil = neues_df[neues_df["Bereich"] == bereich].dropna(subset=["Note"])
 
            if len(teil) > 0:

                schnitt_bereich = (teil["Note"] * teil["ECTS"]).sum() / teil["ECTS"].sum()

                st.write(f"➡️ {bereich}: {schnitt_bereich:.2f}")

            else:

                st.write(f"➡️ {bereich}: keine Noten vorhanden")
 
        st.markdown("---")
 
        # ✅ Praktikum Status

        praktik = neues_df[neues_df["Bereich"] == "Praktikum"]
 
        if praktik["Bestanden"].iloc[0] == True:

            st.success("✅ Praktikum bestanden")

        elif praktik["Bestanden"].iloc[0] == False:

            st.error("❌ Praktikum nicht bestanden")

        else:

            st.warning("⚠️ Praktikum noch nicht bewertet")
 