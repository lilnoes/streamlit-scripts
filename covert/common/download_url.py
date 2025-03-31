import streamlit as st
import pandas as pd


def download_callback(url_input: str, session_state_key: str):
    if not url_input:
        return
    try:
        df = pd.read_json(url_input, lines=True, dtype=object, convert_dates=False)
        st.session_state[session_state_key] = df
        st.session_state["original_df"] = df.copy()
    except Exception as e:
        st.error(f"Error downloading from URL: {str(e)}")


def download_from_url(
    url_input_text: str,
    download_text: str,
    session_state_key: str = "df",
    key="downloa_file",
):
    url_input = st.text_input(url_input_text)
    st.button(
        download_text,
        on_click=download_callback,
        args=(url_input, session_state_key),
        key=key,
    )
