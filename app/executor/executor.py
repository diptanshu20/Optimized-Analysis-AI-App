import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import contextlib
import re

def clean_code(code: str) -> str:
    code = code.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)
    return code.strip()

def preprocess_code(code: str) -> str:
    code = re.sub(r"^\s*import\s+pandas.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*import\s+matplotlib.*$", "", code, flags=re.MULTILINE)
    code = re.sub(r"^\s*import\s+seaborn.*$", "", code, flags=re.MULTILINE)
    return code.strip()

def execute_code(code: str, df: pd.DataFrame):
    local_vars = {
        "df": df.copy(),
        "pd": pd,
        "plt": plt,
        "sns": sns,
    }

    # Set larger figure size & dpi for clearer plots
    plt.rcParams['figure.figsize'] = (12, 7)
    plt.rcParams['figure.dpi'] = 100

    code = clean_code(code)
    code = preprocess_code(code)

    stdout = io.StringIO()
    stderr = io.StringIO()

    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        try:
            exec(code, {}, local_vars)
        except Exception as e:
            return None, None, f"{type(e).__name__}: {e}"

    new_dfs = {}
    for var_name, val in local_vars.items():
        if isinstance(val, pd.DataFrame):
            new_dfs[var_name] = val

    fig = None
    for val in local_vars.values():
        if hasattr(val, "get_figure"):
            fig = val.get_figure()
            plt.close(fig)
            break
    if not fig:
        figs = [plt.figure(n) for n in plt.get_fignums()]
        if figs:
            fig = figs[-1]
            plt.close(fig)

    output_str = stdout.getvalue().strip()

    main_output = local_vars.get("result", None)
    if main_output is None:
        if fig:
            main_output = fig
        elif output_str:
            main_output = output_str
        else:
            main_output = None

    return main_output, new_dfs, None
