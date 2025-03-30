import streamlit as st
import requests
import pandas as pd

from covert.scripts.types.file_types import FileType
from covert.scripts.files_processing.converters.to_jsonl import main as to_jsonl
from covert.scripts.files_processing.converters.to_json import main as to_json
from covert.scripts.files_processing.converters.to_csv import main as to_csv
from covert.utils.dataframes import bytes_to_dataframe


def upload_file_callback():
    uploaded_file = st.session_state["uploaded_file"]
    chosen_file, chosen_file_type = bytes_to_dataframe(uploaded_file.read())
    st.session_state["chosen_file"] = chosen_file
    st.session_state["chosen_file_type"] = chosen_file_type


def main():
    st.title("File Converter")

    # generate a helper text here
    st.markdown("")

    if "chosen_file" not in st.session_state:
        st.session_state["chosen_file"] = pd.DataFrame()
    if "chosen_file_type" not in st.session_state:
        st.session_state["chosen_file_type"] = None

    st.file_uploader(
        "Choose a file", on_change=upload_file_callback, key="uploaded_file"
    )
    url_input = st.text_input("File URL")
    if st.button("Download URL") and url_input:
        resp = requests.get(url_input)
        chosen_file, chosen_file_type = bytes_to_dataframe(resp.content)
        st.session_state["chosen_file"] = chosen_file
        st.session_state["chosen_file_type"] = chosen_file_type

    chosen_file = st.session_state["chosen_file"]
    chosen_file_type = st.session_state["chosen_file_type"]

    if chosen_file.empty:
        st.warning("Please upload a file or enter a URL")
        return

    convert_to = st.selectbox("Convert to", FileType)

    if convert_to == FileType.CSV:
        to_csv(chosen_file)
    elif convert_to == FileType.JSON:
        to_json(chosen_file)
    elif convert_to == FileType.JSONL:
        to_jsonl(chosen_file)
    else:
        st.error(f"Conversion not supported: {chosen_file_type} -> {convert_to}")
