import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def extract_quoted_columns(query: str) -> list:
    return re.findall(r'["\'](.*?)["\']', query)


def generate_code_from_query(user_query: str, df_columns: list) -> str:
    quoted_cols = extract_quoted_columns(user_query)

    prompt = f"""
    You are a data analysis assistant. The user is working with a pandas DataFrame named `df`.

    Here are the actual column names in the DataFrame:
    {df_columns}

    The user mentioned the following column names in quotes:
    {quoted_cols if quoted_cols else '[]'}

    🚫 IMPORTANT CONSTRAINTS:
    - Only use the DataFrame `df` uploaded by the user. Do NOT assume or generate new data.
    - DO NOT create or assume any DataFrame like `df2`, `df3`, or `new_df` unless explicitly requested.
    - DO NOT create any DataFrame with sample data.
    - DO NOT include any import statements (pandas, matplotlib, seaborn) — these are pre-imported.
    - DO NOT use print statements.
    - Instead, assign your final output to a variable named `result`.
    - Use matplotlib or seaborn for plots (but NO plt.show()).
    - Always use the column names exactly (including spaces, casing, underscores).
    - Always try to avoid this error :: Error during code execution: name 'df_columns' is not defined

    📌 Task:
    Generate Python code (only code, no explanation) that performs this task on the user's DataFrame:

    "{user_query}"

    If the task is not possible due to missing columns or unclear instruction, return a comment explaining the problem.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
