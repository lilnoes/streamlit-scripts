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
    if not row_schema:
        return None
    try:
        # Create JSONata expression from schema
        expression = jsonata.Jsonata(row_schema)

        # Transform each row in the dataframe
        transformed_rows = []
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            transformed_row = expression.evaluate(row_dict)
            transformed_rows.append(transformed_row)

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
    st.title("JSONL to CSV")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    row_schema = st.text_area("Row Schema")

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
