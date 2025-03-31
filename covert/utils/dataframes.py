import pandas as pd
from io import StringIO

from covert.scripts.types.file_types import FileType


def get_nested_keys(d: dict, parent_key: str = "") -> list[str]:
    """
    Get all nested keys from a dictionary using dot notation.

    Args:
        d: The dictionary to analyze
        parent_key: The parent key prefix (used in recursion)

    Returns:
        A list of strings representing all nested keys
    """
    keys = []
    for key, value in d.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            keys.extend(get_nested_keys(value, new_key))
        else:
            keys.append(new_key)
    return keys


def get_nested_value(d: dict, path: str):
    """
    Get a value from a nested dictionary using a dot-separated path or a simple key.

    Args:
        d: The dictionary to search in
        path: The dot-separated path to the value, or a simple key

    Returns:
        The value at the specified path, or None if the path doesn't exist
    """
    if "." not in path:
        return d.get(path)

    keys = path.split(".")
    current = d
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None


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
        # Check if column is object type and has at least one row
        if df[col].dtype == "object" and len(df) > 0:
            # Try to get the first non-null value
            first_val = df[col].iloc[0]

            # Check if the first value is a dictionary
            if isinstance(first_val, dict):
                # Get nested keys using get_nested_keys and prefix with column name
                dict_keys = [f"{col}.{key}" for key in get_nested_keys(first_val)]
                keys.extend(dict_keys)

    return keys


def bytes_to_dataframe(data: bytes) -> tuple[pd.DataFrame, FileType | None]:
    text = data.decode("utf-8", errors="replace").strip()

    # Try JSON
    try:
        df = pd.read_json(StringIO(text))
        if not df.empty:
            return df, (FileType.JSON if len(df) == 1 else FileType.JSONL)
    except Exception as e:
        print(e)
        pass

    # Try CSV
    try:
        df = pd.read_csv(StringIO(text))
        if not df.empty:
            return df, FileType.CSV
    except Exception:
        pass

    return pd.DataFrame(), None
