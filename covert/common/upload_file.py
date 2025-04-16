import streamlit as st
import pandas as pd


def update_state_callback(
    session_state_key: str, key: str, original_key: str, file_type: str
):
    uploaded_file = st.session_state[key]
    if not uploaded_file:
        return
    df = pd.read_json(uploaded_file, lines=True, dtype=object, convert_dates=False)
    st.session_state[session_state_key] = df
    st.session_state[original_key] = df.copy()


def upload_file(
    file_text: str,
    session_state_key: str = "df",
    key: str = "upload_file",
    original_key: str = "original_df",
    file_type: str = "jsonl",
):
    st.file_uploader(
        file_text,
        type=file_type,
        on_change=update_state_callback,
        key=f"{key}_file_uploader",
        args=(session_state_key, f"{key}_file_uploader", original_key, file_type),
    )
