import streamlit as st
import pandas as pd


def upload_file(file_text: str, session_state_key: str = "df"):
    uploaded_file = st.file_uploader(file_text, type="jsonl")
    if uploaded_file:
        df = pd.read_json(uploaded_file, lines=True, dtype=object, convert_dates=False)
        st.toast(f"Successfully downloaded {uploaded_file.name}")
        st.session_state[session_state_key] = df
