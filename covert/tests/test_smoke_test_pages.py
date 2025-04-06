from streamlit.testing.v1 import AppTest
import unittest
from covert.app import pages


class TestSmokeTestPages(unittest.TestCase):
    def test_smoke_test_pages(self):
        """
        Test that all pages are linked in the sidebar, and no exceptions are raised.
        """
        app = AppTest.from_file("covert/app.py", default_timeout=100).run()
        links = app.get("page_link")
        pages_count = [1 for items in pages.values() for _ in items]
        self.assertEqual(len(links), sum(pages_count))
