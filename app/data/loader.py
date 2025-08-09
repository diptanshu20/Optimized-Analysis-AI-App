import pandas as pd

def load_data(uploaded_file):
    if uploaded_file is None:
        return None

    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == 'csv':
        try:
            # Try reading assuming CSV has headers
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            # fallback encoding
            df = pd.read_csv(uploaded_file, encoding='latin1')

        # Uncomment this line if your CSV files do NOT have headers and the first row is data:
        # df = pd.read_csv(uploaded_file, header=None)

    elif file_type in ['xlsx', 'xls']:
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

    return df
