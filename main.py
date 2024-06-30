import random
import pandas as pd
import streamlit as st
import functions as fn



data= fn.get_transactions()

columns = ["Datum", "Typ", "Kategorie", "Betrag", "Beschreibung"]

df = pd.DataFrame(data, columns=columns)

st.dataframe(
    df,
    column_config={
        "Betrag": st.column_config.NumberColumn(
            "Betrag",
            help="The price of the product in CHF",
            format="%d CHF",
        ),

    },
    hide_index=True,
)