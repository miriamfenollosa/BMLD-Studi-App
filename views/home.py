import streamlit as st

name = st.session_state.get("name")
vorname = name.split()[0] if name else ""

st.title(f"Willkommen {vorname} 👋!")
st.markdown("Remember why you started.")



# !! WICHTIG: Eure Emails müssen in der App erscheinen!!

st.title('BMI Rechner')

st.markdown("Die Anwendung ermöglicht es Ihnen, Ihren BMI zu berechnen")

st.info("""Der BMI ist ein Screening-Tool, aber keine Diagnose für Körperfett oder Gesundheit.
Bitte konsultieren Sie einen Arzt für eine vollständige Beurteilung.""")

st.write("Diese App wurde von Samuel Wehrli (wehs@zhaw.ch) im Rahmen des Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")