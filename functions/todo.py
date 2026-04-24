import pandas as pd

def add_todo(df, date, text):
    new_row = {
        "Datum": date,
        "Eintrag": text,
        "Erledigt": False
    }
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

def remove_done(df):
    return df[df["Erledigt"] == False].reset_index(drop=True)
