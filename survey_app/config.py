import streamlit as st

def setup_page_config():
    st.set_page_config(
        page_title=str(st.session_state.page_header),
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
