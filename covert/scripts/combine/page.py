from covert.common.file_uploader import file_uploader
from covert.states.file_state import FileState
import streamlit as st


def main():
    st.title("Combine")
    st.text("Combine data from multiple files")
    st.divider()

    uploaded_file = file_uploader()

    if uploaded_file:
        st.write("yay")
