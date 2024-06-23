import streamlit as st
import functions as fn

st.write("hello world")
bank = fn.get_bank()
st.table(bank)
