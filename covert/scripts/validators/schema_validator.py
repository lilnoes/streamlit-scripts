import streamlit as st
import pandas as pd
from genson import SchemaBuilder

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.utils.string_utils import is_uuid
from covert.utils.validate_schema import validate_schema
from covert.utils.dataframes import get_keys, get_nested_value


def get_init_schema(df: pd.DataFrame, index: int) -> dict:
    """
    Generate an initial JSON schema from the dataframe.
    Detects UUID values and adds appropriate format.

    Args:
        df: DataFrame to generate schema from
        index: Index of the row to use for generating schema
    Returns:
        JSON schema as dictionary
    """
    keys = get_keys(df)
    row = df.iloc[index].to_dict()

    # Create base schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
    }

    # Check for UUID values in the specified row
    for key in keys:
        value = get_nested_value(row, key)

        # Create nested structure for the key
        path = key.split(".")
        current = schema["properties"]

        # Build the nested structure
        for i, part in enumerate(path):
            if i < len(path) - 1:
                if part not in current:
                    current[part] = {"type": "object", "properties": {}}
                if "properties" not in current[part]:
                    current[part]["properties"] = {}
                current = current[part]["properties"]
            else:
                # We're at the final property
                if isinstance(value, str) and is_uuid(value):
                    current[part] = {"type": "string", "format": "uuid"}
                # Don't add non-UUID fields

    return schema


def data_preview_fragment(name: str, df: pd.DataFrame):
    data_preview(df, prefix_key=f"diff_files_{name}", title=f"Preview of {name} data")


def main():
    st.title("Schema validator")

    # generate a helper text here
    st.markdown("""
    """)

    upload_file("Choose a file (JSONL)", "df", "df", file_type="jsonl")
    upload_file(
        "Choose a schema (JSON) (optional)", "schema", "schema", file_type="json"
    )

    if "df" not in st.session_state or st.session_state.df.empty:
        st.warning("Please upload a file")
        st.stop()

    if "schema" not in st.session_state:
        schema = None
    else:
        schema = st.session_state.schema

    df = st.session_state.df

    data_preview_fragment("File", df)

    if not schema:
        index = st.selectbox(
            "Select an index to use for generating schema", list(range(len(df)))
        )
        row = df.iloc[int(index)].to_dict()
        with st.expander("Selected row"):
            st.json(row)
        builder = SchemaBuilder()
        builder.add_schema(get_init_schema(df, index))
        builder.add_object(row)
        generated_schema = builder.to_schema()
        with st.expander("Generated schema"):
            st.json(generated_schema)

        if st.button("Validate schema"):
            data = [(i, row) for i, row in enumerate(df.to_dict("records"))]
            errors = validate_schema(generated_schema, data)
            with st.expander("Validation errors"):
                st.json(errors)


if __name__ == "__main__":
    main()
