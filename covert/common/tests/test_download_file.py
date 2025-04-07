from streamlit.testing.v1 import AppTest
import tempfile
import os
import pytest


@pytest.fixture
def sample_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b'{"id": 1, "name": "test1"}\n{"id": 2, "name": "test2"}')
    temp_file.close()
    yield temp_file.name
    os.unlink(temp_file.name)


@pytest.fixture
def sample_app():
    # Define test app that uses the original function with patched uploader
    def test_app():
        from covert.common.download_url import download_from_url
        import pandas as pd
        import streamlit as st

        download_from_url("Enter URL", "Download")

    # Create AppTest instance
    app = AppTest.from_function(test_app)
    return app


def test_download_file(sample_app, sample_file):
    """Test the download_file function"""
    # Run the app
    sample_app.run()

    # Initial state check - DataFrames should not exist yet
    assert "df" not in sample_app.session_state
    assert "original_df" not in sample_app.session_state

    sample_app.get("text_input")[0].input(sample_file).run()
    sample_app.get("button")[0].click().run()

    # Check if session state was updated
    assert "df" in sample_app.session_state
    assert "original_df" in sample_app.session_state

    # test if df has 2 rows
    assert len(sample_app.session_state["df"]) == 2
