import pandas as pd
import unittest
from unittest.mock import patch
from covert.scripts.files_processing.remove_tasks_by_key import remove_tasks
from streamlit.testing.v1 import AppTest


class TestRemoveTasks(unittest.TestCase):
    def setUp(self):
        """Create a sample DataFrame with both flat and nested data structures."""
        data = [
            {"id": "task1", "content": "First task", "metadata": {"uuid": "uuid1"}},
            {"id": "task2", "content": "Second task", "metadata": {"uuid": "uuid2"}},
            {"id": "task3", "content": "Third task", "metadata": {"uuid": "uuid3"}},
            {"id": "task4", "content": "Fourth task", "metadata": {"uuid": "uuid4"}},
        ]
        self.sample_df = pd.DataFrame(data)

    def test_remove_tasks_main(self):
        app = AppTest.from_file(
            "covert/scripts/files_processing/remove_tasks_by_key.py"
        ).run()
        app.session_state.df = self.sample_df
        app.run()
        app.selectbox[0].select("id")
        app.text_area[0].input("task1\ntask3").run()

        # Remove tasks
        [button for button in app.button if button.label == "Remove Tasks"][
            0
        ].click().run()

        # Save filtered file
        [button for button in app.button if button.label == "Save Filtered File"][
            0
        ].click().run()

        # Check that the filtered file has the correct rows
        filtered_df = app.session_state.df
        self.assertEqual(len(filtered_df), 2)
        self.assertNotIn("task1", filtered_df["id"].values)
        self.assertNotIn("task3", filtered_df["id"].values)
        self.assertIn("task2", filtered_df["id"].values)
        self.assertIn("task4", filtered_df["id"].values)

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_direct_key(self, mock_toast, mock_warning):
        """Test removing tasks using a direct (non-nested) key."""
        # Remove tasks with IDs task1 and task3
        result_df = remove_tasks(self.sample_df, ["task1", "task3"], "id")

        # Check that only 2 rows remain
        self.assertEqual(len(result_df), 2)

        # Check that the correct rows were removed
        self.assertNotIn("task1", result_df["id"].values)
        self.assertNotIn("task3", result_df["id"].values)
        self.assertIn("task2", result_df["id"].values)
        self.assertIn("task4", result_df["id"].values)

        # Check that toast was called with correct message
        mock_toast.assert_called_once_with("Entered 2 IDs to remove. Removed 2 tasks.")
        mock_warning.assert_not_called()

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_nested_key(self, mock_toast, mock_warning):
        """Test removing tasks using a nested key."""
        # Remove tasks with nested UUIDs uuid2 and uuid4
        result_df = remove_tasks(self.sample_df, ["uuid2", "uuid4"], "metadata.uuid")

        # Check that only 2 rows remain
        self.assertEqual(len(result_df), 2)

        # Check that the correct rows were removed
        self.assertNotIn("task2", result_df["id"].values)
        self.assertNotIn("task4", result_df["id"].values)
        self.assertIn("task1", result_df["id"].values)
        self.assertIn("task3", result_df["id"].values)

        # Check that toast was called with correct message
        mock_toast.assert_called_once_with("Entered 2 IDs to remove. Removed 2 tasks.")
        mock_warning.assert_not_called()

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_empty_ids(self, mock_toast, mock_warning):
        """Test behavior when no IDs are provided to remove."""
        # Call with empty list of IDs
        result_df = remove_tasks(self.sample_df, [], "id")

        # Should return original DataFrame unchanged
        pd.testing.assert_frame_equal(result_df, self.sample_df)

        # Should show warning
        mock_warning.assert_called_once_with("Please enter at least one ID to remove.")
        mock_toast.assert_not_called()

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_nonexistent_ids(self, mock_toast, mock_warning):
        """Test removing tasks with IDs that don't exist in the DataFrame."""
        # Try to remove non-existent IDs
        result_df = remove_tasks(self.sample_df, ["task99", "task100"], "id")

        # Should return original DataFrame unchanged
        pd.testing.assert_frame_equal(result_df, self.sample_df)

        # Should show toast with 0 removed
        mock_toast.assert_called_once_with("Entered 2 IDs to remove. Removed 0 tasks.")
        mock_warning.assert_not_called()

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_nonexistent_key(self, mock_toast, mock_warning):
        """Test removing tasks with a key that doesn't exist in the DataFrame."""
        # Try to remove using a non-existent key
        result_df = remove_tasks(self.sample_df, ["value1"], "nonexistent_key")

        # Should return original DataFrame unchanged
        pd.testing.assert_frame_equal(result_df, self.sample_df)

        # Should show toast with 0 removed
        mock_toast.assert_called_once_with("Entered 1 IDs to remove. Removed 0 tasks.")
        mock_warning.assert_not_called()

    @patch("streamlit.warning")
    @patch("streamlit.toast")
    def test_remove_tasks_with_mixed_results(self, mock_toast, mock_warning):
        """Test removing tasks with a mix of existing and non-existing IDs."""
        # Try to remove one existing and one non-existing ID
        result_df = remove_tasks(self.sample_df, ["task1", "task99"], "id")

        # Should remove only the existing ID
        self.assertEqual(len(result_df), 3)
        self.assertNotIn("task1", result_df["id"].values)

        # Should show toast with 1 removed
        mock_toast.assert_called_once_with("Entered 2 IDs to remove. Removed 1 tasks.")
        mock_warning.assert_not_called()
