import streamlit as st
import branding
import pandas as pd
import functions as fn
import login
import loginfunctions as lfn

st.set_page_config(
    page_title="Konten",
    page_icon="🏦",
)

branding.loadBranding()

login.SetLoginSessionState()

LOGGED_IN = st.session_state.login
user = st.session_state.user_id
username = lfn.get_username(user)

if LOGGED_IN == True:
    bankAccounts = fn.get_bankAccounts(user)
    tabs = st.tabs([account[1] for account in bankAccounts])
    for i, tab in enumerate(tabs):
            with tab:
                data= fn.get_transactions(bankAccounts[i][0])
                columns = ["Datum", "Typ", "Kategorie", "Betrag", "Beschreibung"]

                df = pd.DataFrame(data, columns=columns)

                st.title(bankAccounts[i][1])
                st.write(f"Kontostand: **{bankAccounts[i][2]}**")
                st.write(f"IBAN: **{bankAccounts[i][3]}**")
                st.write(f"Bank: **{bankAccounts[i][4]}**")
                st.dataframe(
                    df,
                    column_config={
                        "Betrag": st.column_config.NumberColumn(
                            "Betrag",
                            help="The price of the product in CHF",
                            format="%.2f CHF",
                        ),
                        "Datum": st.column_config.DateColumn(
                             "Datum",
                             format="DD.MM.YYYY",
                        ),

                    },
                    hide_index=True,
                )