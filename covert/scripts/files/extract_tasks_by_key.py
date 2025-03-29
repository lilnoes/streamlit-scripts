import streamlit as st
import pandas as pd

from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys


def extract_tasks_callback(ids_to_extract, id_key):
    if not ids_to_extract:
        st.warning("Please enter at least one ID to extract.")
        return

    df = st.session_state.df

    if "." in id_key:
        # Handle nested keys (e.g., "metadata.id")
        parent_key, child_key = id_key.split(".", 1)
        # Filter rows where the nested key matches any ID in the list
        filtered_df = df[
            df[parent_key].apply(
                lambda x: (
                    x.get(child_key) in ids_to_extract if isinstance(x, dict) else False
                )
            )
        ]
    else:
        # Filter rows where the key matches any ID in the list
        filtered_df = df[df[id_key].isin(ids_to_extract)]

    # Count extracted items
    extracted_count = len(filtered_df)

    # Update session state
    st.session_state.df = filtered_df

    st.toast(
        f"Entered {len(ids_to_extract)} IDs to extract. Extracted {extracted_count} tasks."
    )


def restore_original_file_callback():
    st.session_state.df = st.session_state.original_df


def main():
    st.title("Extract Tasks By Key")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df
    original_df = st.session_state.original_df

    if not df.empty:
        st.write(df.head(5))

    st.divider()

    if st.button("View All"):
        st.header("All Data")
        st.write(df)
        st.divider()

    keys = get_keys(df)

    id_key = st.selectbox("Select Key", keys)

    ids_to_extract_text = st.text_area("IDs to Extract")

    ids_to_extract = ids_to_extract_text.split("\n")
    ids_to_extract = [id.strip() for id in ids_to_extract if id.strip()]

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Extract Tasks",
            on_click=extract_tasks_callback,
            args=(ids_to_extract, id_key),
        )

    with col2:
        st.button("Restore Original file", on_click=restore_original_file_callback)

    if not df.empty and st.button("Download Extracted Data"):
        # Convert DataFrame to JSONL
        jsonl_data = df.to_json(orient="records", lines=True)

        # Provide download button
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name="extracted_tasks.jsonl",
            mime="application/jsonl",
        )
