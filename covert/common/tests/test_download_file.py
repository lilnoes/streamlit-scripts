import unittest
from streamlit.testing.v1 import AppTest
import tempfile
import os


class TestDownloadFile(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary file with test data
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b'{"id": 1, "name": "test1"}\n{"id": 2, "name": "test2"}')
        self.url = self.temp_file.name
        self.temp_file.close()

        # Define test app that uses the original function with patched uploader
        def test_app():
            from covert.common.download_url import download_from_url
            import pandas as pd
            import streamlit as st

            download_from_url("Enter URL", "Download")

        # Create AppTest instance
        self.app = AppTest.from_function(test_app)

    def tearDown(self):
        """Clean up after each test"""
        # Delete the temporary file
        if hasattr(self, "temp_file") and os.path.exists(self.url):
            os.unlink(self.url)

    def test_download_file(self):
        """Test the download_file function"""
        # Run the app
        self.app.run()

        # Initial state check - DataFrames should not exist yet
        self.assertNotIn("df", self.app.session_state)
        self.assertNotIn("original_df", self.app.session_state)

        self.app.get("text_input")[0].input(self.url).run()
        self.app.get("button")[0].click().run()

        # Check if session state was updated
        self.assertIn("df", self.app.session_state)
        self.assertIn("original_df", self.app.session_state)

        # test if df has 2 rows
        self.assertEqual(len(self.app.session_state["df"]), 2)
