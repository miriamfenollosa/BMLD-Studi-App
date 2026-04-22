import pandas as pd

def berechne_schnitt(df):
    gültig = df.dropna(subset=["Note"])
    
    if len(gültig) == 0:
        return None
    
    return (gültig["Note"] * gültig["ECTS"]).sum() / gültig["ECTS"].sum()


def berechne_bereichsschnitt(df, bereich):
    teil_df = df[df["Bereich"] == bereich]
    return berechne_schnitt(teil_df)


def prüfe_praktikum(df):
    praktik = df[df["Bereich"] == "Praktikum"]
    
    if praktik.empty:
        return None
    
    status = praktik["Bestanden"].iloc[0]
    
    if status == True:
        return "bestanden"
    elif status == False:
        return "nicht bestanden"
    else:
        return "offen"
