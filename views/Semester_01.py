import streamlit as st
import pandas as pd
 
st.title("1. Semester")
 
# Fächer mit einer Note

single_subjects = ["Bio", "HäHä", "MeMi", "Sys", "GeDa", "Englisch", "GKS"]
 
# Fächer mit mehreren Noten

multi_subjects = ["Chemie", "Mathe", "Informatik"]
grades = {}
 
st.header("Einzelnoten")
 
for subject in single_subjects:

    grades[subject] = st.number_input(

        f"{subject} Note",
        min_value=1.0,
        max_value=6.0,
        step=0.1,
        key=subject
    )
 
st.header("Mehrere Noten")
 
for subject in multi_subjects:

    st.subheader(subject)

    subject_grades = []

    for i in range(3):  # 3 Eingaben pro Fach

        grade = st.number_input(

            f"{subject} Note {i+1}",
            min_value=1.0,
            max_value=6.0,
            step=0.1,
            key=f"{subject}_{i}"
        )

        subject_grades.append(grade)

    grades[subject] = subject_grades
 
# Daten in Tabelle umwandeln

data = []
 
for subject in single_subjects:

    data.append([subject, grades[subject]])
 
for subject in multi_subjects:

    avg = sum(grades[subject]) / len(grades[subject])

    data.append([subject, round(avg, 2)])
 
df = pd.DataFrame(data, columns=["Fach", "Durchschnittsnote"])
 
st.header("Übersicht")

st.dataframe(df)
 