import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value


def remove_tasks_callback(ids_to_remove: list[str], id_key: str) -> None:
    if not ids_to_remove:
        st.warning("Please enter at least one ID to remove.")
        return

    df = st.session_state.df

    # Filter out rows where the key (nested or direct) matches any ID in the list
    filtered_df = df[
        ~df.apply(
            lambda row: get_nested_value(row.to_dict(), id_key) in ids_to_remove, axis=1
        )
    ]

    # Count removed items
    removed_count = len(df) - len(filtered_df)

    # Update session state
    st.session_state.df = filtered_df

    st.toast(
        f"Entered {len(ids_to_remove)} IDs to remove. Removed {removed_count} tasks."
    )


def restore_original_file_callback():
    st.session_state.df = st.session_state.original_df


def main():
    st.title("Remove Tasks By Key")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df
    original_df = st.session_state.original_df

    data_preview(df)

    keys = get_keys(df)

    id_key = st.selectbox("Select Key", keys)

    ids_to_remove_text = st.text_area("IDs to Remove")

    ids_to_remove = ids_to_remove_text.split("\n")
    ids_to_remove = [id.strip() for id in ids_to_remove if id.strip()]

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Remove Tasks",
            on_click=remove_tasks_callback,
            args=(ids_to_remove, id_key),
        )

    with col2:
        st.button("Restore Original file", on_click=restore_original_file_callback)

    if not df.empty and st.button("Download Filtered Data"):
        # Convert DataFrame to JSONL
        jsonl_data = df.to_json(orient="records", lines=True)

        # Provide download button
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name="filtered_tasks.jsonl",
            mime="application/jsonl",
        )
