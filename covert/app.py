import streamlit as st
import pandas as pd
from covert.scripts.files.remove_ids import main as remove_ids_main

# from scripts.default.default import main as default_main

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "original_df" not in st.session_state:
    st.session_state.original_df = pd.DataFrame()

pages = {
    "Files Processing": [
        st.Page(
            remove_ids_main,
            title="Remove IDs",
            icon=":material/arrow_back_ios:",
            url_path="/files-remove_ids",
        ),
    ]
}

st.sidebar.title("Covert Exports")
with st.sidebar:
    for index, (key, values) in enumerate(pages.items()):
        expander = st.sidebar.expander(key)
        for page in values:
            expander.page_link(page)
        if index < len(pages) - 1:
            st.sidebar.divider()

pg = st.navigation(pages)
pg.run()
