import streamlit as st
import re

def display_generated_code(code: str):
    if not code:
        return

    # Remove markdown triple backticks and optional language tag
    cleaned_code = code.strip()
    if cleaned_code.startswith("```"):
        lines = cleaned_code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned_code = "\n".join(lines)

    st.subheader("Generated Code")
    st.code(cleaned_code, language="python")
