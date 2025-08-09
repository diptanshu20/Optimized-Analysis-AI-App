import streamlit as st
from app.components.dataframe_buttons import upload_file
from app.data.loader import load_data
from app.state.state_manager import StateManager
from app.components.chat import user_chat_input
from app.components.code_box import display_generated_code
from app.api.gemini_client import generate_code_from_query
from app.executor.executor import execute_code
import matplotlib.pyplot as plt
import re

# Initialize or retrieve StateManager instance from session state
if "state_manager" not in st.session_state:
    st.session_state.state_manager = StateManager()

state = st.session_state.state_manager

def parse_save_dataframe_command(user_query):
    """
    Parse commands like 'save this as dataframe df2' to extract the new dataframe name.
    """
    pattern = r"save\s+(?:this|the result|it)\s+as\s+(?:dataframe\s+)?(\w+)"
    match = re.search(pattern, user_query, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def main():
    st.title("Data Analysis App")

    left_col, right_col = st.columns([1, 1])

    with left_col:
        # File upload
        uploaded_file = upload_file()
        if uploaded_file:
            df = load_data(uploaded_file)
            if df is not None:
                state.set_original_df(df)
                st.success("Data loaded successfully!")

        # DataFrame selector dropdown
        if state.dataframes:
            selected_df_key = st.selectbox(
                "Select active DataFrame",
                list(state.dataframes.keys()),
                index=list(state.dataframes.keys()).index(state.current_df_key),
            )
            if selected_df_key != state.current_df_key:
                state.switch_dataframe(selected_df_key)

        # Show columns of current dataframe
        current_df = state.get_current_df()
        if current_df is not None:
            with st.expander("Show Available Columns"):
                st.write(list(current_df.columns))

        # User input for query
        user_query = user_chat_input()

        # Run query button
        run_query = st.button("Run Query")

        generated_code = ""
        exec_output = None
        exec_error = None
        new_dfs = {}

        if run_query and user_query and current_df is not None:
            df_columns = list(current_df.columns)

            with st.spinner("Generating code..."):
                try:
                    generated_code = generate_code_from_query(user_query, df_columns)
                except Exception as e:
                    st.error(f"Error generating code: {e}")

            if generated_code:
                with st.spinner("Executing code..."):
                    exec_output, new_dfs, exec_error = execute_code(generated_code, current_df)

            # Detect "save as dataframe" commands and save new dataframe
            new_df_name = parse_save_dataframe_command(user_query)
            if new_df_name and new_dfs:
                for df_name, df_val in new_dfs.items():
                    if df_name != "df":
                        if new_df_name in state.dataframes:
                            st.warning(f"DataFrame '{new_df_name}' already exists. Choose another name.")
                        else:
                            state.add_dataframe(new_df_name, df_val)
                            state.switch_dataframe(new_df_name)
                            st.success(f"DataFrame saved as '{new_df_name}'")
                        break

        # Show generated code to user
        display_generated_code(generated_code)

        # Show execution error if any
        if exec_error:
            st.error(f"Error during code execution:\n{exec_error}")

    with right_col:
        current_df = state.get_current_df()
        if current_df is not None:
            st.subheader(f"Showing DataFrame: {state.current_df_key}")
            st.dataframe(current_df.head(10))

        if not exec_error:
            if exec_output is not None:
                if hasattr(exec_output, "get_figure"):
                    st.pyplot(exec_output.get_figure())
                elif isinstance(exec_output, plt.Figure):
                    st.pyplot(exec_output)
                else:
                    st.text_area("Output", value=str(exec_output), height=300)

if __name__ == "__main__":
    main()
