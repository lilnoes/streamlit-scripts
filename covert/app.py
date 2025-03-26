import streamlit as st
from covert.scripts.backfill.page import main as backfill_main
from covert.scripts.combine.page import main as combine_main

# from scripts.default.default import main as default_main

pages = {
    "Files Processing": [
        st.Page(
            backfill_main,
            title="Backfill",
            icon=":material/arrow_back_ios:",
            url_path="/backfill",
        ),
        st.Page(
            combine_main,
            title="Combine",
            icon=":material/arrow_back_ios:",
            url_path="/combine",
        ),
        st.Page(
            "scripts/default/default.py",
            title="Default",
            icon=":material/arrow_back_ios:",
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
