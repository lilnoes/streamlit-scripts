from streamlit.testing.v1 import AppTest
from covert.app import pages_list
import pandas as pd
import pytest


def test_smoke_test_whole_app():
    """
    Test that all pages are linked in the sidebar, and no exceptions are raised.
    """
    app = AppTest.from_file("covert/app.py", default_timeout=100).run()
    links = app.get("page_link")
    assert len(links) == len(pages_list)
    assert list(app.exception) == []


@pytest.mark.parametrize("script", [page.script for page in pages_list])
def test_smoke_test_single_page(script):
    """
    Test that all pages can be run without exceptions.
    """
    app = AppTest.from_file(f"covert/{script}", default_timeout=100)
    app.session_state.df = pd.DataFrame()
    app.session_state.df_original = pd.DataFrame()
    app.run()
    assert list(app.exception) == []
    assert app.session_state.df is not None
    title = app.title
    assert len(title) > 0
