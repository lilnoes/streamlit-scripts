import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from ydata_profiling import ProfileReport


def main():
    st.title("Pandas Profiler")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    if st.button("Get summary"):
        pr = ProfileReport(df, title="Pandas Profiler Report")
        t = pr.to_html()
        st.html(t)
