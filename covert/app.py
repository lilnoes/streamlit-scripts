import streamlit as st
import pandas as pd
from covert.scripts.files_processing.remove_tasks_by_key import (
    main as remove_tasks_by_key_main,
)
from covert.scripts.files_processing.extract_tasks_by_key import (
    main as extract_tasks_by_key_main,
)
from covert.scripts.files_processing.split_tasks_by_key import (
    main as split_tasks_by_key_main,
)
from covert.scripts.files_processing.converter import main as converter_main
from covert.scripts.files_processing.extract_keys import main as extract_keys_main
from covert.scripts.files_processing.duplicates_remover import (
    main as duplicates_remover_main,
)
from covert.scripts.validators.latex import main as latex_main
from covert.scripts.validators.profiler import main as profiler_main

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "original_df" not in st.session_state:
    st.session_state.original_df = pd.DataFrame()

pages = {
    "Files Processing": [
        st.Page(
            remove_tasks_by_key_main,
            title="Remove Tasks By Key",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-remove_tasks_by_key",
        ),
        st.Page(
            extract_tasks_by_key_main,
            title="Extract Tasks By Key",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-extract_tasks_by_key",
        ),
        st.Page(
            split_tasks_by_key_main,
            title="Split Tasks By Key",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-split_tasks_by_key",
        ),
        st.Page(
            converter_main,
            title="File Converter",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-converter",
        ),
        st.Page(
            extract_keys_main,
            title="Extract Keys",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-extract_keys",
        ),
        st.Page(
            duplicates_remover_main,
            title="Duplicates Remover",
            icon=":material/arrow_back_ios:",
            url_path="/files-processing-duplicates_remover",
        ),
    ],
    "Validators": [
        st.Page(
            latex_main,
            title="LaTeX Validator",
            icon=":material/arrow_back_ios:",
            url_path="/validators-latex",
        ),
        st.Page(
            profiler_main,
            title="Pandas Profiler",
            icon=":material/arrow_back_ios:",
            url_path="/validators-profiler",
        ),
    ],
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
