import pandas as pd
from unittest.mock import patch
from covert.scripts.files_processing.extract_tasks_by_key import extract_tasks
from streamlit.testing.v1 import AppTest
import pytest


@pytest.fixture
def sample_df():
    data = [
        {"id": "task1", "content": "First task", "metadata": {"uuid": "uuid1"}},
        {"id": "task2", "content": "Second task", "metadata": {"uuid": "uuid2"}},
        {"id": "task3", "content": "Third task", "metadata": {"uuid": "uuid3"}},
        {"id": "task4", "content": "Fourth task", "metadata": {"uuid": "uuid4"}},
    ]
    return pd.DataFrame(data)


def test_extract_tasks_main(sample_df):
    app = AppTest.from_file(
        "covert/scripts/files_processing/extract_tasks_by_key.py"
    ).run()
    app.session_state.df = sample_df
    app.run()
    app.selectbox[0].select("id")
    app.text_area[0].input("task1\ntask3").run()

    # Extract tasks
    [button for button in app.button if button.label == "Extract Tasks"][
        0
    ].click().run()

    # Save extracted file
    [button for button in app.button if button.label == "Save Extracted File"][
        0
    ].click().run()

    # Check that the extracted file has the correct rows
    extracted_df = app.session_state.df
    assert len(extracted_df) == 2
    assert "task1" in extracted_df["id"].values
    assert "task3" in extracted_df["id"].values
    assert "task2" not in extracted_df["id"].values
    assert "task4" not in extracted_df["id"].values


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_direct_key(mock_toast, mock_warning, sample_df):
    """Test extracting tasks using a direct (non-nested) key."""
    # Extract tasks with IDs task1 and task3
    result_df = extract_tasks(sample_df, ["task1", "task3"], "id")

    # Check that only 2 rows remain
    assert len(result_df) == 2

    # Check that the correct rows were removed
    assert "task1" in result_df["id"].values
    assert "task3" in result_df["id"].values
    assert "task2" not in result_df["id"].values
    assert "task4" not in result_df["id"].values

    # Check that toast was called with correct message
    mock_toast.assert_called_once_with("Entered 2 IDs to extract. Extracted 2 tasks")
    mock_warning.assert_not_called()


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_nested_key(mock_toast, mock_warning, sample_df):
    """Test extracting tasks using a nested key."""
    # Extract tasks with nested UUIDs uuid2 and uuid4
    result_df = extract_tasks(sample_df, ["uuid2", "uuid4"], "metadata.uuid")

    # Check that only 2 rows remain
    assert len(result_df) == 2

    # Check that the correct rows were extracted
    assert "task2" in result_df["id"].values
    assert "task4" in result_df["id"].values
    assert "task1" not in result_df["id"].values
    assert "task3" not in result_df["id"].values

    # Check that toast was called with correct message
    mock_toast.assert_called_once_with("Entered 2 IDs to extract. Extracted 2 tasks")
    mock_warning.assert_not_called()


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_empty_ids(mock_toast, mock_warning, sample_df):
    """Test behavior when no IDs are provided to extract."""
    # Call with empty list of IDs
    result_df = extract_tasks(sample_df, [], "id")

    # Should return original DataFrame unchanged
    pd.testing.assert_frame_equal(result_df, sample_df)

    # Should show warning
    mock_warning.assert_called_once_with("Please enter at least one ID to extract.")
    mock_toast.assert_not_called()


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_nonexistent_ids(mock_toast, mock_warning, sample_df):
    """Test extracting tasks with IDs that don't exist in the DataFrame."""
    # Try to extract non-existent IDs
    result_df = extract_tasks(sample_df, ["task99", "task100"], "id")

    # Remove all rows
    empty_df = sample_df.iloc[0:0]
    pd.testing.assert_frame_equal(result_df, empty_df)

    # Should show toast with 0 extracted
    mock_toast.assert_called_once_with("Entered 2 IDs to extract. Extracted 0 tasks")
    mock_warning.assert_not_called()


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_nonexistent_key(mock_toast, mock_warning, sample_df):
    """Test extracting tasks with a key that doesn't exist in the DataFrame."""
    # Try to extract using a non-existent key
    result_df = extract_tasks(sample_df, ["value1"], "nonexistent_key")

    # Remove all rows
    empty_df = sample_df.iloc[0:0]
    pd.testing.assert_frame_equal(result_df, empty_df)

    # Should show toast with 0 extracted
    mock_toast.assert_called_once_with("Entered 1 IDs to extract. Extracted 0 tasks")
    mock_warning.assert_not_called()


@patch("streamlit.warning")
@patch("streamlit.toast")
def test_extract_tasks_with_mixed_results(mock_toast, mock_warning, sample_df):
    """Test extracting tasks with a mix of existing and non-existing IDs."""
    # Try to extract one existing and one non-existing ID
    result_df = extract_tasks(sample_df, ["task1", "task99"], "id")

    # Should extract only the existing ID
    assert len(result_df) == 1
    assert "task1" in result_df["id"].values

    # Should show toast with 1 extracted
    mock_toast.assert_called_once_with("Entered 2 IDs to extract. Extracted 1 tasks")
    mock_warning.assert_not_called()
