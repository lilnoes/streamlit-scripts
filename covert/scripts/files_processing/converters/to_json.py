import streamlit as st
import pandas as pd
import io
import json

from covert.common.data_preview import data_preview
from covert.utils.transform import transform_data


@st.fragment
def preview_data(json_data):
    st.header("Preview of transformed data:")
    try:
        preview_df = pd.read_json(io.StringIO(json_data))
        data_preview(preview_df, prefix_key="to_json")
    except Exception as e:
        st.error(f"Error previewing JSON data: {str(e)}")
        st.text(json_data[:1000] + "..." if len(json_data) > 1000 else json_data)


def to_json(df: pd.DataFrame, row_schema: str):
    try:
        if not row_schema:
            output = io.StringIO()
            df.to_json(output, orient="records")
            return output.getvalue()

        transformed_rows = transform_data(df, row_schema)

        if len(transformed_rows) != 1:
            return {"items": transformed_rows}
        return transformed_rows[0]

    except Exception as e:
        st.error(f"Error transforming data: {str(e)}")
        return None


def main():
    df = st.session_state["chosen_file"]

    row_schema = st.text_area(
        "Row Schema",
        help="""
        The row schema is a JSONata expression that describes the structure of the data in the file.
        It is used to transform the data into a JSON format.
        (If empty, the data will be converted to JSON Lines without transformation)
        """,
    )

    if st.button("Convert to JSON"):
        json_data = to_json(df, row_schema)
        if json_data:
            preview_data(json_data)

            # Add download button
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="transformed_data.json",
                mime="application/json",
            )
