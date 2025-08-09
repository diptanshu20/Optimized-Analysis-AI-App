import streamlit as st

def user_chat_input():
    """
    Returns user input string from a text area.
    """
    return st.text_area("Ask your question here:", height=100)
