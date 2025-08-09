import streamlit as st

def upload_file():
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xlsx', 'xls'])
    return uploaded_file

def dataframe_switcher(df_keys, current_key):
    """
    Display buttons to switch between dataframes.
    Returns the selected key.
    """
    if not df_keys:
        return None

    st.subheader("Switch DataFrames")
    selected = st.radio("Select DataFrame", options=df_keys, index=df_keys.index(current_key))
    return selected
