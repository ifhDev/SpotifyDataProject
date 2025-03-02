def create_binary_classification(df, new_col_name, base_col, percentile_cutoff):
    """
    Converts a numerical column into a binary classification based on a percentile cutoff.

    Parameters:
    df (pd.DataFrame): The dataset
    new_col_name (str): Name of the new binary column
    base_col (str): The column to base classification on
    percentile_cutoff (float): The percentile threshold (e.g., 67 for top 33%)

    Returns:
    pd.DataFrame: Updated DataFrame with new binary column
    """
    df[new_col_name] = (df[base_col] >= percentile_cutoff).astype(int)
    return df