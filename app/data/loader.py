import pandas as pd

def load_data(uploaded_file):
    if uploaded_file is None:
        return None

    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'csv':
        try:
            # Important: Reset file pointer to start before reading
            uploaded_file.seek(0)

            # Read CSV, explicitly specify UTF-8 encoding (you can try 'utf-8-sig' if BOM issues)
            df = pd.read_csv(uploaded_file, encoding='utf-8')

        except UnicodeDecodeError:
            # fallback encoding
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='latin1')

    elif file_type in ['xlsx', 'xls']:
        # Reset pointer and read excel
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

    return df
