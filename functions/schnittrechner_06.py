import streamlit as st

import pandas as pd
 
st.title("📚 Notenschnittrechner (Semester)")
 
st.write("Trage deine Module und Noten ein:")
 
# Standard-Module (kannst du anpassen)

module = [

    "Mathematik",

    "Chemie",

    "Biologie",

    "Informatik",

    "Deutsch",

    "Englisch"

]
 
# DataFrame erstellen (Session speichern!)

if "df" not in st.session_state:

    st.session_state.df = pd.DataFrame({

        "Modul": module,

        "Note": [None] * len(module),

        "ECTS": [1] * len(module)  # Gewichtung (optional)

    })
 
df = st.session_state.df
 
# Tabelle bearbeiten

edited_df = st.data_editor(

    df,

    num_rows="dynamic",

    use_container_width=True

)
 
# Aktualisieren im Session State

st.session_state.df = edited_df
 
# Berechnung

if st.button("Semesterschnitt berechnen"):

    # Nur gültige Noten nehmen

    gültige_noten = edited_df.dropna(subset=["Note"])
 
    if len(gültige_noten) == 0:

        st.error("Bitte mindestens eine Note eingeben.")

    else:

        # Gewichteter Schnitt

        durchschnitt = (

            (gültige_noten["Note"] * gültige_noten["ECTS"]).sum()

            / gültige_noten["ECTS"].sum()

        )
 
        st.success(f"📊 Dein Semesterschnitt ist: {durchschnitt:.2f}")
 
 