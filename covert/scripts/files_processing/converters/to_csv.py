import streamlit as st
import pandas as pd
import io
import csv

from covert.common.data_preview import data_preview
from covert.utils.transform import transform_data


@st.fragment
def preview_data(csv_data):
    st.header("Preview of transformed data:")
    preview_df = pd.read_csv(io.StringIO(csv_data))
    data_preview(preview_df, prefix_key="jsonl_to_csv")


def to_csv(df, row_schema):
    try:
        if not row_schema:
            # Direct conversion to CSV without transformation
            output = io.StringIO()
            df.to_csv(output, index=False)
            return output.getvalue()

        transformed_rows = transform_data(df, row_schema)

        # Get all unique keys from transformed data
        all_keys = set()
        for row in transformed_rows:
            all_keys.update(row.keys())

        # Create CSV in memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(all_keys))
        writer.writeheader()
        writer.writerows(transformed_rows)

        return output.getvalue()

    except Exception as e:
        st.error(f"Error transforming data: {str(e)}")
        return None


def main():
    df = st.session_state["chosen_file"]

    row_schema = st.text_area(
        "Row Schema",
        help="""
        The row schema is a JSONata expression that describes the structure of the data in the file.
        It is used to transform the data into a CSV format.
        (If empty, the data will be converted to a CSV without transformation) 
        """,
    )

    if st.button("Convert to CSV"):
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
