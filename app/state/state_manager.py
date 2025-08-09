class StateManager:
    def __init__(self):
        self.dataframes = {}  # key: name, value: DataFrame
        self.current_df_key = None

    def set_original_df(self, df):
        self.dataframes['original'] = df
        self.current_df_key = 'original'

    def get_current_df(self):
        if self.current_df_key:
            return self.dataframes.get(self.current_df_key)
        return None

    def add_dataframe(self, key, df):
        self.dataframes[key] = df

    def switch_dataframe(self, key):
        if key in self.dataframes:
            self.current_df_key = key
        else:
            raise KeyError(f"DataFrame with key '{key}' not found")

    def get_all_keys(self):
        return list(self.dataframes.keys())
