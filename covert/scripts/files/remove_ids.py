import streamlit as st
import pandas as pd

from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url


def main():
    st.title("Remove IDs")

    uploaded_file = upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    df = st.session_state.df
    original_df = st.session_state.original_df

    if not df.empty:
        st.write(df.head())

    st.write(df)
