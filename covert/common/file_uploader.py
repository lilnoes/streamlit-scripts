import streamlit as st


def file_uploader(label: str = "Upload a file", type: list[str] = None):
    return st.file_uploader(label, type=type, key="file_uploader")
