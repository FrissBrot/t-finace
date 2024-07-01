import branding
import pandas as pd
import streamlit as st
import functions as fn
import login
import loginfunctions as lfn

branding.loadBranding()

login.SetLoginSessionState()

LOGGED_IN = st.session_state.login
user = st.session_state.user_id
username = lfn.get_username(user)

if LOGGED_IN == True:
    st.title("Herzlich Willkommen " + username +"!")
    fn.get_bankAccounts(user)

    transactionTypes = fn.get_transactionsTypes()
    transactionCategories = fn.get_transactionsCategories()


    with st.form("Transaktion erfassen"):
        st.markdown("### Transaktion erfassen")
        form_transactionDate = st.date_input("Datum:", format="DD.MM.YYYY")
        form_transactionType = st.selectbox("Typ:", (transactionTypes))
        form_transactionCategory = st.selectbox("Kategorie:", (transactionCategories))
        form_transactionAmount = st.number_input("Betrag in CHF")
        form_transactionDescrition = st.text_input("Beschreibung")
        submitted_add_transaction = st.form_submit_button("Transaktion erfassen")

        if submitted_add_transaction:
            category_id = fn.get_transactionCategory_id(form_transactionCategory)
            type_id = fn.get_transactionType_id(form_transactionType)
            fn.add_transaction(1, type_id, category_id, 3, 2, form_transactionDate, form_transactionAmount, form_transactionDescrition)



    # Transaction Table
    data= fn.get_transactions(3)

    columns = ["Datum", "Typ", "Kategorie", "Betrag", "Beschreibung"]

    df = pd.DataFrame(data, columns=columns)

    st.dataframe(
        df,
        column_config={
            "Betrag": st.column_config.NumberColumn(
                "Betrag",
                help="The price of the product in CHF",
                format="%.2f CHF",
            ),

        },
        hide_index=True,
    )
else: st.switch_page("pages/login.py")