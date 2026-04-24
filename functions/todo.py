import pandas as pd

def add_todo(df, date, entry):
    new_row = pd.DataFrame([{
        "Datum": pd.to_datetime(date),
        "Eintrag": str(entry),
        "Erledigt": False
    }])

    return pd.concat([df, new_row], ignore_index=True)


def remove_done(df):
    return df[df["Erledigt"] == False].reset_index(drop=True)
