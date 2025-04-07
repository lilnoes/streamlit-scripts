from streamlit.testing.v1 import AppTest


def test_upload_file():
    """Test the upload_file function with a patched st.file_uploader"""

    # Define test app that uses the original function with patched uploader
    def test_app():
        from covert.common.upload_file import upload_file
        from unittest.mock import patch
        import streamlit as st
        import json
        import io

        def mock_file_uploader(label, type, key, on_change=None, args=(), **kwargs):
            if st.button(f"Mock {label}", key=f"mock_button_{key}"):
                # Create mock JSONL data
                mock_data = [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]
                jsonl_string = "\n".join(json.dumps(item) for item in mock_data)
                mock_file = io.BytesIO(jsonl_string.encode())

                st.session_state[key] = mock_file

                # Call the callback if provided
                if on_change:
                    on_change(*args)

                return mock_file
            return None

        with patch("streamlit.file_uploader", side_effect=mock_file_uploader):
            upload_file("JSONL File", "test_df", "test_upload", "test_original_df")

    # Create AppTest instance
    app = AppTest.from_function(test_app).run()

    # Initial state check - DataFrames should not exist yet
    assert "test_df" not in app.session_state
    assert "test_original_df" not in app.session_state

    app.get("button")[0].click().run()

    # Check if session state was updated
    assert "test_df" in app.session_state
    assert "test_original_df" in app.session_state
