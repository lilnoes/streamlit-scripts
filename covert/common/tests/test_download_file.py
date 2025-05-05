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
def sample_app(request):
    key1, key2 = getattr(request, "param")

    # Define test app that uses the original function with patched uploader
    def test_app(key1, key2):
        from covert.common.download_url import download_from_url
        import pandas as pd
        import streamlit as st

        download_from_url(
            "Enter URL", "Download", session_state_key=f"state_key_{key1}", key=key1
        )
        download_from_url(
            "Enter URL", "Download", session_state_key=f"state_key_{key2}", key=key2
        )

    # Create AppTest instance
    app = AppTest.from_function(test_app, args=(key1, key2))
    app.session_state.params = (key1, key2)
    return app


@pytest.mark.parametrize(
    "sample_app", [("key1", "key2"), ("key2", "key1")], indirect=True
)
def test_download_file(sample_app, sample_file):
    """Test the download_file function"""
    # Run the app
    sample_app.run()
    assert len(sample_app.exception) == 0
    key1, _ = sample_app.session_state["params"]
    state_key1 = f"state_key_{key1}"

    # Initial state check - DataFrames should not exist yet
    assert state_key1 not in sample_app.session_state
    assert "original_df" not in sample_app.session_state

    sample_app.get("text_input")[0].input(sample_file).run()
    sample_app.get("button")[0].click().run()

    # Check if session state was updated
    assert state_key1 in sample_app.session_state
    assert "original_df" in sample_app.session_state

    # test if df has 2 rows
    assert len(sample_app.session_state[state_key1]) == 2


@pytest.mark.parametrize("sample_app", [("key", "key")], indirect=True)
def test_multiple_elements(sample_app, sample_file):
    """Test the case where there are multiple elements with the same key"""
    # Run the app
    sample_app.run()
    exception = sample_app.exception[0]
    # Check if the exception message contains the expected error message
    assert "There are multiple elements with the same" in exception.message
