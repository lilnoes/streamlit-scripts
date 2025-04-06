import json
import streamlit as st
import pandas as pd
import io

from covert.common.data_preview import data_preview
from covert.utils.transform import transform_data


@st.fragment
def preview_data(jsonl_data):
    st.header("Preview of transformed data:")
    try:
        preview_df = pd.read_json(io.StringIO(jsonl_data), lines=True)
        data_preview(preview_df, prefix_key="to_jsonl")
    except Exception as e:
        st.error(f"Error previewing JSONL data: {str(e)}")
        st.text(jsonl_data[:1000] + "..." if len(jsonl_data) > 1000 else jsonl_data)


def to_jsonl(df, row_schema):
    try:
        if not row_schema:
            output = io.StringIO()
            df.to_json(output, orient="records", lines=True)
            return output.getvalue()

        transformed_rows = transform_data(df, row_schema)

        output_lines = []
        for row in transformed_rows:
            output_lines.append(json.dumps(row))

        return "\n".join(output_lines)

    except Exception as e:
        st.error(f"Error transforming data: {str(e)}")
        return None


def main():
    df = st.session_state["chosen_file"]

    row_schema = st.text_area(
        "Row Schema",
        help="""
        The row schema is a JSONata expression that describes the structure of the data in the file.
        It is used to transform the data into a JSONL format.
        (If empty, the data will be converted to JSONL without transformation)
        """,
    )

    if st.button("Convert to JSONL"):
        jsonl_data = to_jsonl(df, row_schema)
        if jsonl_data:
            preview_data(jsonl_data)

            # Add download button
            st.download_button(
                label="Download JSONL",
                data=jsonl_data,
                file_name="transformed_data.jsonl",
                mime="application/json-lines",
            )
