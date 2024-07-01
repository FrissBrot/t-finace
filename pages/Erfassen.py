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
    transactionTypes = fn.get_transactionsTypes()
    transactionCategories = fn.get_transactionsCategories()
    bankAccounts_raw = fn.get_bankAccounts(user)
    
    bankAccounts = []
    for row in bankAccounts_raw:
        bankAccounts.append(row[1])

    with st.form("Transaktion erfassen"):
            st.markdown("### Transaktion erfassen")
            form_bankAccount = st.selectbox("Konto:", (bankAccounts))
            form_transactionDate = st.date_input("Datum:", format="DD.MM.YYYY")
            form_transactionType = st.selectbox("Typ:", (transactionTypes))
            form_transactionCategory = st.selectbox("Kategorie:", (transactionCategories))
            form_transactionAmount = st.number_input("Betrag in CHF")
            form_transactionDescrition = st.text_input("Beschreibung")
            submitted_add_transaction = st.form_submit_button("Transaktion erfassen")

            if submitted_add_transaction:
                category_id = fn.get_transactionCategory_id(form_transactionCategory)
                type_id = fn.get_transactionType_id(form_transactionType)
                bankAccount_id = fn.get_transactionBankAccount_id(form_bankAccount)
                #Betrag negativieren
                if type_id == 10 or type_id == 7:
                    form_transactionAmount = -abs(form_transactionAmount)

                #Transaktion speichern
                fn.add_transaction(user, type_id, category_id, bankAccount_id, 2, form_transactionDate, form_transactionAmount, form_transactionDescrition)