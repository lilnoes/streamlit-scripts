import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value


def update_rename_key(key: str):
    new_name = st.session_state[f"rename_{key}"]
    if not new_name:
        return
    st.session_state.rename_mapping[key] = new_name


@st.fragment
def extracted_preview(df: pd.DataFrame, extraction_keys: list[str]):
    extracted_df = extract_keys(df, extraction_keys)
    extraction_keys = [
        st.session_state.rename_mapping.get(key, key) for key in extraction_keys
    ]
    st.write("Extracted data:")

    # Show JSON and Python list formats
    with st.expander("JSON Format"):
        json_data = extracted_df.to_json(orient="records", indent=2)
        st.code(json_data, language="json")

    with st.expander("Python List Format"):
        if len(extraction_keys) == 1:
            values = [
                f'"{value}"' for value in extracted_df[extraction_keys[0]].tolist()
            ]
            python_list = "[\n    " + ",\n    ".join(values) + "\n]"
        else:
            rows = []
            for _, row in extracted_df.iterrows():
                values = [f'"{row[key]}"' for key in extraction_keys]
                rows.append("[" + ", ".join(values) + "]")
            python_list = "[\n    " + ",\n    ".join(rows) + "\n]"
        st.code(python_list, language="python")

    # Download options
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "Download CSV",
            extracted_df.to_csv(index=False),
            "extracted_data.csv",
            "text/csv",
        )

    with col2:
        st.download_button(
            "Download JSON",
            extracted_df.to_json(orient="records"),
            "extracted_data.json",
            "application/json",
        )

    with col3:
        st.download_button(
            "Download JSONL",
            extracted_df.to_json(orient="records", lines=True),
            "extracted_data.jsonl",
            "application/jsonl",
        )


def extract_keys(df: pd.DataFrame, extraction_keys: list[str]) -> pd.DataFrame:
    if not extraction_keys:  # Handle empty keys case
        return df

    result = {}
    for key in extraction_keys:
        # Use renamed column or original key if no rename exists
        new_name = st.session_state.rename_mapping.get(key, key)
        result[new_name] = df.apply(lambda row: get_nested_value(row, key), axis=1)

    return pd.DataFrame(result)


def main():
    st.title("Extract keys from file")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    if "rename_mapping" not in st.session_state:
        st.session_state.rename_mapping = {}

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    extraction_keys = st.multiselect("Select Keys", keys)

    if extraction_keys:
        st.subheader("Rename Columns")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Original Key**")
            for key in extraction_keys:
                st.text(key)

        with col2:
            st.markdown("**New Name**")
            for key in extraction_keys:
                st.text_input(
                    "##",
                    key=f"rename_{key}",
                    value=st.session_state.rename_mapping.get(key, key),
                    label_visibility="collapsed",
                    on_change=update_rename_key,
                    args=(key,),
                )

    if st.button("Extract Keys"):
        if not extraction_keys:
            st.warning("Please select at least one key to extract")
        else:
            extracted_preview(df, extraction_keys)
