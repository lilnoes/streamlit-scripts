import streamlit as st
import pandas as pd


def download_from_url(
    url_input_text: str, download_text: str, session_state_key: str = "df"
):
    url_input = st.text_input(url_input_text)
    if st.button(download_text) and url_input:
        try:
            df = pd.read_json(url_input, lines=True, dtype=object, convert_dates=False)
            st.toast(f"Successfully downloaded data from URL")
            st.session_state[session_state_key] = df
        except Exception as e:
            st.error(f"Error downloading from URL: {str(e)}")
