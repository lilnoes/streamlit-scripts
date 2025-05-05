import streamlit as st

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.utils.dataframes import get_keys, get_nested_value
import pandas as pd


def save_extracted_file_callback(df: pd.DataFrame):
    st.session_state.df = df
    st.toast("Extracted file saved")


@st.fragment
def download_fragment(extracted_df: pd.DataFrame):
    jsonl_data = extracted_df.to_json(orient="records", lines=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Save Extracted File",
            on_click=save_extracted_file_callback,
            args=(extracted_df,),
            help="Save the extracted file for future use",
        )
    with col2:
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name="extracted_tasks.jsonl",
            mime="application/jsonl",
        )


@st.fragment
def data_preview_fragment(df: pd.DataFrame):
    st.header("Preview of extracted data:")
    data_preview(df, prefix_key="extract_tasks_by_key")


def extract_tasks(
    df: pd.DataFrame, ids_to_extract: list[str], id_key: str
) -> pd.DataFrame:
    if not ids_to_extract:
        st.warning("Please enter at least one ID to extract.")
        return df

    # Extract rows where the key (nested or direct) matches any ID in the list
    extracted_df = df[
        df.apply(
            lambda row: get_nested_value(row.to_dict(), id_key) in ids_to_extract,
            axis=1,
        )
    ]
    message = f"Entered {len(ids_to_extract)} IDs to extract. Extracted {len(extracted_df)} tasks"
    st.toast(message)

    return extracted_df


def restore_original_file_callback():
    st.session_state.df = st.session_state.original_df


def main():
    st.title("Extract Tasks By Key")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    id_key = st.selectbox("Select Key", keys)

    ids_to_extract_text = st.text_area("IDs to Extract")

    ids_to_extract = ids_to_extract_text.split("\n")
    ids_to_extract = [id.strip() for id in ids_to_extract if id.strip()]

    if st.button("Extract Tasks"):
        extracted_df = extract_tasks(df, ids_to_extract, id_key)
        data_preview_fragment(extracted_df)
        download_fragment(extracted_df)

    st.button("Restore Original file", on_click=restore_original_file_callback)


if __name__ == "__main__":
    main()
