import re
import pandas as pd
from io import BytesIO

from covert.scripts.types.file_types import FileType


def get_file_type(name: str) -> FileType:
    name = name.lower().strip()
    if re.search(r"\.csv[?]?$", name):
        return FileType.CSV
    elif re.search(r"\.json[?]?$", name):
        return FileType.JSON
    elif re.search(r"\.jsonl[?]?$", name):
        return FileType.JSONL
    return FileType.UNKNOWN


def get_df(data: bytes | str, file_name: str) -> pd.DataFrame:
    """
    Get DataFrame from data based on file name.

    Args:
        data: Raw data as bytes or string
        file_name: Name of the file to determine type

    Returns:
        pd.DataFrame: Parsed data
    """
    file_type = get_file_type(file_name)
    if file_type == FileType.CSV:
        return read_csv(data)
    elif file_type == FileType.JSON:
        return read_json(data)
    elif file_type == FileType.JSONL:
        return read_jsonl(data)
    return pd.DataFrame()


def read(data: bytes | str, file_type: FileType, **kwargs) -> pd.DataFrame:
    """
    Read bytes into a DataFrame based on file type.

    Args:
        bytes_data: Raw bytes to read
        file_type: Type of file (CSV, JSON, JSONL)
        **kwargs: Additional arguments to pass to the reader

    Returns:
        pd.DataFrame: Parsed data
    """
    if file_type == FileType.CSV:
        return read_csv(data)
    elif file_type == FileType.JSON:
        orient = kwargs.get("orient", "records")
        return read_json(data, orient)
    elif file_type == FileType.JSONL:
        return read_jsonl(data)
    else:
        return pd.DataFrame()


def read_csv(data: bytes | str) -> pd.DataFrame:
    """Read CSV bytes into a DataFrame."""
    if isinstance(data, str):
        return pd.read_csv(data)
    return pd.read_csv(BytesIO(data))


def read_json(data: bytes | str, orient: str = "records") -> pd.DataFrame:
    """
    Read JSON into a DataFrame with optional orient parameter.

    Args:
        data: Raw data as bytes or string
        orient: Orientation of JSON data structure

    Returns:
        pd.DataFrame: Parsed data
    """
    if isinstance(data, str):
        return pd.read_json(data, orient=orient)
    return pd.read_json(BytesIO(data), orient=orient)


def read_jsonl(data: bytes | str) -> pd.DataFrame:
    """
    Read JSONL (JSON Lines) into a DataFrame.

    Args:
        data: Raw data as bytes or string

    Returns:
        pd.DataFrame: Parsed data
    """
    if isinstance(data, str):
        return pd.read_json(data, lines=True)
    return pd.read_json(BytesIO(data), lines=True)
