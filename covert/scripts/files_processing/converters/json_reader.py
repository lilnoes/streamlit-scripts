import enum
import streamlit as st
import pandas as pd
from io import StringIO

from covert.scripts.types.file_types import FileType


class OrientMethod(str, enum.Enum):
    """JSON orientation methods for pandas read_json"""

    RECORDS = "records"
    SPLIT = "split"
    INDEX = "index"
    COLUMNS = "columns"
    VALUES = "values"
    TABLE = "table"


def read_json_callback(orient_method: OrientMethod):
    """Callback to read JSON with specified orientation"""
    try:
        text = (
            st.session_state["chosen_file_bytes"]
            .decode("utf-8", errors="replace")
            .strip()
        )
        df = pd.read_json(StringIO(text), orient=orient_method)
        st.session_state["chosen_file"] = df
        st.toast(f"Successfully loaded JSON with {orient_method} orientation")
    except Exception as e:
        st.error(f"Error reading JSON: {str(e)}")


def main():
    chosen_file_type = st.session_state["chosen_file_type"]
    chosen_file = st.session_state["chosen_file"]
    print(chosen_file_type)

    if not chosen_file.empty and chosen_file_type == FileType.JSON:
        orient_method = st.selectbox(
            "JSON Open method",
            options=OrientMethod,
            help="Select the orientation method for reading the JSON file",
        )

        st.button(
            "Load JSON",
            on_click=read_json_callback,
            args=(orient_method,),
            help="Click to load the JSON file with selected orientation",
        )
