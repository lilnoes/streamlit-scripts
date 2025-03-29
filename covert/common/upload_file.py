import streamlit as st
import pandas as pd


def update_state_callback(session_state_key: str):
    uploaded_file = st.session_state["upload_file"]
    df = pd.read_json(uploaded_file, lines=True, dtype=object, convert_dates=False)
    st.session_state[session_state_key] = df
    st.session_state["original_df"] = df.copy()


def upload_file(file_text: str, session_state_key: str = "df"):
    st.file_uploader(
        file_text,
        type="jsonl",
        on_change=update_state_callback,
        key="upload_file",
        args=(session_state_key,),
    )
