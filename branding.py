import streamlit as st
import toastfunction as to

def loadBranding():
    #Toast anzeigen falls vorhanden.
    to.viev_toast()

    #initialize sessions
    if 'login' not in st.session_state:
        st.session_state.login = False
        print("session new created")

    if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        
    if 'redirect' not in st.session_state:
        st.session_state.redirect = None

    # Hide streamlit branding
    #hide_streamlit_style = "<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>"
    #st.markdown(hide_streamlit_style, unsafe_allow_html=True)