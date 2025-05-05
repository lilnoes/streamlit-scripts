import streamlit as st
import pandas as pd

from covert.utils.files import get_df


def update_state_callback(
    session_state_key: str, key: str, original_key: str, file_type: list[str]
):
    uploaded_file = st.session_state[key]
    if not uploaded_file:
        return
    df = get_df(uploaded_file.getvalue(), uploaded_file.name)
    st.session_state[session_state_key] = df
    st.session_state[original_key] = df.copy()


def upload_file(
    file_text: str,
    session_state_key: str = "df",
    key: str = "upload_file",
    original_key: str = "original_df",
    file_type: list[str] = ["jsonl"],
):
    st.file_uploader(
        file_text,
        type=file_type,
        on_change=update_state_callback,
        key=f"{key}_file_uploader",
        args=(session_state_key, f"{key}_file_uploader", original_key, file_type),
    )
