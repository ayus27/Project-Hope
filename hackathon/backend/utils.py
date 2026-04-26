import pandas as pd


def summarize_dataframe(df: pd.DataFrame, max_rows: int = 5) -> str:
    """Return a short summary of a DataFrame for debug and dashboard display."""
    return df.head(max_rows).to_markdown(index=False)
