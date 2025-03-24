import streamlit as st
from covert.scripts.backfill.page import main as backfill_main
from covert.scripts.combine.page import main as combine_main

# from scripts.default.default import main as default_main

pages = [
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
        "scripts/default/default.py", title="Default", icon=":material/arrow_back_ios:"
    ),
]

pg = st.navigation(pages)
pg.run()
