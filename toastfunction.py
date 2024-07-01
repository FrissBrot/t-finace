import streamlit as st

def set_toast(toast, icon):
    if 'toast' not in st.session_state:
        st.session_state.toast = ""
    if 'toast_icon' not in st.session_state:
        st.session_state.toast_icon = ""
    
    st.session_state.toast = toast
    st.session_state.toast_icon = icon

def viev_toast():
    if 'toast' in st.session_state:
        if not st.session_state.toast == "":
            message = st.session_state.toast
            icon_from_session = st.session_state.toast_icon
            st.toast(message, icon=icon_from_session)

            st.session_state.toast = ""
            st.session_state.toast_icon = ""