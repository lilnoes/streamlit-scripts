import streamlit as st
import requests
import pandas as pd

from covert.common.data_preview import data_preview
from covert.scripts.types.file_types import FileType
from covert.scripts.files_processing.converters.to_jsonl import main as to_jsonl
from covert.scripts.files_processing.converters.to_json import main as to_json
from covert.scripts.files_processing.converters.to_csv import main as to_csv
from covert.scripts.files_processing.converters.json_reader import main as json_reader
from covert.utils.files import read, get_file_type


def save_file_to_session(file_name: str, file_bytes: bytes):
    if not file_name:
        return
    chosen_file_type = get_file_type(file_name)
    st.session_state["chosen_file_type"] = chosen_file_type
    if chosen_file_type == FileType.UNKOWN:
        st.session_state["chosen_file_type"] = FileType.UNKOWN
        st.error(f"Unknown file type: {file_name}")
        return

    chosen_file = read(file_bytes, chosen_file_type)
    st.session_state["chosen_file"] = chosen_file
    st.session_state["chosen_file_bytes"] = file_bytes


def upload_file_callback():
    uploaded_file = st.session_state["uploaded_file"]
    save_file_to_session(uploaded_file.name, uploaded_file.read())


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
        save_file_to_session(url_input, resp.content)

    chosen_file = st.session_state["chosen_file"]
    chosen_file_type = st.session_state["chosen_file_type"]

    if chosen_file.empty:
        st.warning("Please upload a file or enter a URL")
        return

    json_reader()

    data_preview(chosen_file)

    convert_to = st.selectbox(
        "Convert to", [FileType.CSV.value, FileType.JSON.value, FileType.JSONL.value]
    )

    if convert_to == FileType.CSV:
        to_csv()
    elif convert_to == FileType.JSON:
        to_json()
    elif convert_to == FileType.JSONL:
        to_jsonl()
    else:
        st.error(f"Conversion not supported: {chosen_file_type} -> {convert_to}")
