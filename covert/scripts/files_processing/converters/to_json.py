import streamlit as st
import pandas as pd
import jsonata
import io
import csv

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url


@st.fragment
def preview_data(csv_data):
    st.header("Preview of transformed data:")
    preview_df = pd.read_csv(io.StringIO(csv_data))
    data_preview(preview_df, prefix_key="jsonl_to_csv")


def to_csv(df, row_schema):
    pass


def main(df):

    data_preview(df)

    row_schema = st.text_area("Row Schema")

    if st.button("Convert to JSON"):
        csv_data = to_csv(df, row_schema)
        if csv_data:
            preview_data(csv_data)

            # Add download button
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="transformed_data.csv",
                mime="text/csv",
            )
