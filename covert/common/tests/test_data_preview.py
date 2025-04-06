import pandas as pd
import streamlit as st
from streamlit.testing.v1 import AppTest
import pytest
from covert.common.data_preview import data_previewer, data_preview


# def test_data_preview_basic():
#     """Test basic functionality of data_preview with a small DataFrame"""
#     # Create a test app
#     at = AppTest.from_function(run_data_preview_test)
#     at.run()

#     # Check if the expander exists
#     assert at.expander() is not None

#     # Check if the dataframe is rendered
#     assert at.dataframe() is not None

#     # Check pagination text (should show page 1 of 2)
#     assert "Page 1 of 2" in at.text_elements()[0].value

#     # Test next button functionality
#     next_button = at.button("Next →")
#     assert next_button is not None
#     assert not next_button.disabled

#     # Click next button
#     at.click("Next →")
#     at.run()

#     # Should now be on page 2
#     assert "Page 2 of 2" in at.text_elements()[0].value

#     # Previous button should be enabled, Next button should be disabled
#     assert not at.button("← Previous").disabled
#     assert at.button("Next →").disabled

#     # Click previous button
#     at.click("← Previous")
#     at.run()

#     # Should be back on page 1
#     assert "Page 1 of 2" in at.get_text_elements()[0].value


# def test_data_previewer_custom_render():
#     """Test data_previewer with custom render function"""
#     at = AppTest.from_function(run_data_previewer_custom_test)
#     at.run()

#     # Check if the expander exists
#     assert at.get_expander("Data Preview") is not None

#     # Check if the custom render function was used (should create a table)
#     assert at.get_table() is not None


# def run_data_preview_test():
#     """App function for testing data_preview"""
#     # Create a test DataFrame with 75 rows (should create 2 pages with page_size=50)
#     df = pd.DataFrame({"A": range(75), "B": [f"value_{i}" for i in range(75)]})

#     # Use the data_preview function
#     data_preview(df, page_size=50, prefix_key="test")


# def run_data_previewer_custom_test():
#     """App function for testing data_previewer with custom render function"""
#     # Create a list of 30 items
#     data = list(range(30))

#     # Define a function to get a page of data
#     def get_page(start, end):
#         return data[start:end]

#     # Use data_previewer with a custom render function
#     data_previewer(
#         total_size=len(data),
#         get_page_data=get_page,
#         page_size=20,
#         prefix_key="custom",
#         render_fn=st.table,  # Use table instead of dataframe
#     )


# def test_empty_dataframe():
#     """Test data_preview with an empty DataFrame"""
#     at = AppTest.from_function(run_empty_df_test)
#     at.run()

#     # Should not display anything for empty DataFrame
#     assert len(at.get_expanders()) == 0


# def run_empty_df_test():
#     """App function for testing data_preview with empty DataFrame"""
#     df = pd.DataFrame()
#     data_preview(df)
