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


def read_bytes(bytes_data: bytes, file_type: FileType, **kwargs) -> pd.DataFrame:
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
        return read_csv_bytes(bytes_data)
    elif file_type == FileType.JSON:
        orient = kwargs.get("orient", "records")
        return read_json_bytes(bytes_data, orient)
    elif file_type == FileType.JSONL:
        return read_jsonl_bytes(bytes_data)
    else:
        return pd.DataFrame()


def read_csv_bytes(bytes_data: bytes) -> pd.DataFrame:
    """Read CSV bytes into a DataFrame."""
    return pd.read_csv(BytesIO(bytes_data))


def read_json_bytes(bytes_data: bytes, orient: str = "records") -> pd.DataFrame:
    """Read JSON bytes into a DataFrame with optional orient parameter."""
    return pd.read_json(BytesIO(bytes_data), orient=orient)


def read_jsonl_bytes(bytes_data: bytes) -> pd.DataFrame:
    """Read JSONL (JSON Lines) bytes into a DataFrame."""
    return pd.read_json(BytesIO(bytes_data), lines=True)
