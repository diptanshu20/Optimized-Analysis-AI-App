import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_output(output):
    """
    Display output from code execution:
    - DataFrame shown as table
    - matplotlib Figure shown as plot
    - string shown as text
    - None shows placeholder
    """
    st.subheader("Output")

    if output is None:
        st.info("No output yet.")
    elif isinstance(output, pd.DataFrame):
        st.dataframe(output)
    elif isinstance(output, plt.Figure):
        st.pyplot(output)
    elif isinstance(output, str):
        st.text(output)
    else:
        st.write(output)
