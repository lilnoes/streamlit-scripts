import pandas as pd
import streamlit as st
from io import StringIO, BytesIO

from covert.scripts.types.file_types import FileType


def get_keys(df: pd.DataFrame) -> list[str]:
    """
    Get all column names from a DataFrame, and for columns containing dictionaries,
    also extract the dictionary keys from the first row.

    Args:
        df: The pandas DataFrame to analyze

    Returns:
        A list of strings containing column names and dictionary keys
    """
    keys = []

    # Add all column names
    keys.extend(df.columns.tolist())

    # Check each column for dictionaries
    for col in df.columns:
        # Check if column is object type and has at least one rowF
        if df[col].dtype == "object" and len(df) > 0:
            # Try to get the first non-null value
            first_val = df[col].iloc[0]

            # Check if the first value is a dictionary
            if isinstance(first_val, dict):
                # Add the dictionary keys with the column name as prefix
                dict_keys = [f"{col}.{key}" for key in first_val.keys()]
                keys.extend(dict_keys)

    return keys


def bytes_to_dataframe(data: bytes) -> tuple[pd.DataFrame, FileType]:
    text = data.decode("utf-8", errors="replace").strip()

    # Try JSON
    try:
        df = pd.read_json(StringIO(text))
        if not df.empty:
            return df, FileType.JSON
    except Exception:
        pass

    # Try JSON Lines
    try:
        df = pd.read_json(StringIO(text), lines=True)
        if not df.empty:
            return df, FileType.JSONL
    except Exception:
        pass

    # Try CSV
    try:
        df = pd.read_csv(StringIO(text))
        if not df.empty:
            return df, FileType.CSV
    except Exception:
        pass

    return None, None
