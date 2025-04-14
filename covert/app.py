from pydantic import BaseModel
import streamlit as st
import pandas as pd


if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()
if "original_df" not in st.session_state:
    st.session_state.original_df = pd.DataFrame()


class CustomPage(BaseModel):
    title: str
    icon: str
    url_path: str
    script: str
    category: str


pages_list: list[CustomPage] = [
    CustomPage(
        title="Remove Tasks By Key",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-remove_tasks_by_key",
        script="scripts/files_processing/remove_tasks_by_key.py",
        category="Files Processing",
    ),
    CustomPage(
        title="Extract Tasks By Key",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-extract_tasks_by_key",
        script="scripts/files_processing/extract_tasks_by_key.py",
        category="Files Processing",
    ),
    CustomPage(
        title="Split Tasks By Key",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-split_tasks_by_key",
        script="scripts/files_processing/split_tasks_by_key.py",
        category="Files Processing",
    ),
    CustomPage(
        title="File Converter",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-converter",
        script="scripts/files_processing/converter.py",
        category="Files Processing",
    ),
    CustomPage(
        title="Extract Keys",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-extract_keys",
        script="scripts/files_processing/extract_keys.py",
        category="Files Processing",
    ),
    CustomPage(
        title="Diff Files",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-diff_files",
        script="scripts/files_processing/diff_files.py",
        category="Files Processing",
    ),
    CustomPage(
        title="Duplicates Remover",
        icon=":material/arrow_back_ios:",
        url_path="/files-processing-duplicates_remover",
        script="scripts/files_processing/duplicates_remover.py",
        category="Files Processing",
    ),
    CustomPage(
        title="LaTeX Validator",
        icon=":material/arrow_back_ios:",
        url_path="/validators-latex",
        script="scripts/validators/latex.py",
        category="Validators",
    ),
    CustomPage(
        title="Pandas Profiler",
        icon=":material/arrow_back_ios:",
        url_path="/validators-profiler",
        script="scripts/validators/profiler.py",
        category="Validators",
    ),
]

categories = set([page.category for page in pages_list])

pages = {
    category: [
        st.Page(page.script, title=page.title, icon=page.icon, url_path=page.url_path)
        for page in pages_list
        if page.category == category
    ]
    for category in sorted(categories)
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
