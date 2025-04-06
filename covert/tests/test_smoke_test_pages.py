from streamlit.testing.v1 import AppTest
from covert.app import pages


def test_smoke_test_pages():
    """
    Test that all pages are linked in the sidebar, and no exceptions are raised.
    """
    app = AppTest.from_file("covert/app.py", default_timeout=100).run()
    links = app.get("page_link")
    pages_count = [1 for items in pages.values() for _ in items]
    assert len(links) == sum(pages_count)
