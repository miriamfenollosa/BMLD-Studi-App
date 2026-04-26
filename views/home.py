import streamlit as st

name = st.session_state.get("name")
vorname = name.split()[0] if name else ""

st.title(f"Willkommen {vorname} 👋!")
st.markdown("Remember why you started.")



# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

st.title('BMLD Studi App')

st.markdown("Organisiere deinen Studienalltag mit unserer praktischen App! Verwalte deine To-Do's, deinen Kalender, deinen Stundenplan, berechne deinen Schnitt und behalte deine Hydratation im Auge - alles an einem Ort.")

st.info("""Beachte, dass diese App für Vollzeitstudierende im Normalmodus konzipiert ist, sie ist weniger für Teilzeitstudierende oder Studierende des verkürzten Modus geeignet.""")

st.write("Diese App wurde von Laura Gjugja, Miriam Ilak de Brito und Miriam Fenollosa Muñoz im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")