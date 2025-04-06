import streamlit as st
import pandas as pd
from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value


@st.fragment
def data_preview_fragment(df: pd.DataFrame):
    st.header("Preview of filtered data:")
    data_preview(df, prefix_key="remove_tasks_by_key")


@st.fragment
def download_fragment(filtered_df: pd.DataFrame, jsonl_data: str):
    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Save Filtered File",
            on_click=save_filtered_file_callback,
            args=(filtered_df,),
            help="Save the filtered file for future use",
        )
    with col2:
        st.download_button(
            label="Download JSONL",
            data=jsonl_data,
            file_name="filtered_tasks.jsonl",
            mime="application/jsonl",
        )


def remove_tasks(
    df: pd.DataFrame, ids_to_remove: list[str], id_key: str
) -> pd.DataFrame:
    if not ids_to_remove:
        st.warning("Please enter at least one ID to remove.")
        return df

    # Filter out rows where the key (nested or direct) matches any ID in the list
    filtered_df = df[
        ~df.apply(
            lambda row: get_nested_value(row.to_dict(), id_key) in ids_to_remove, axis=1
        )
    ]

    # Count removed items
    removed_count = len(df) - len(filtered_df)

    st.toast(
        f"Entered {len(ids_to_remove)} IDs to remove. Removed {removed_count} tasks."
    )

    return filtered_df


def save_filtered_file_callback(df: pd.DataFrame):
    st.session_state.df = df
    st.toast("Filtered file saved")


def restore_original_file_callback():
    st.session_state.df = st.session_state.original_df
    st.toast("Original file restored")


def main():
    st.title("Remove Tasks By Key")
    with st.expander("Help"):
        st.markdown(
            """
            ## 🔍 Task Removal Tool
            
        This script allows you to remove tasks from a JSONL file based on a key:
        
        - 📤 Upload a file or download from a URL
        - 🔑 Select a key to filter by
        - 📝 Enter IDs to remove
        - 💾 Save the filtered file for future use
        - 🔄 Restore the original file
        - 📊 Preview the filtered data
        - 📥 Download the filtered file
        """
        )

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    id_key = st.selectbox("Select Key", keys)

    ids_to_remove_text = st.text_area("IDs to Remove")

    ids_to_remove = ids_to_remove_text.split("\n")
    ids_to_remove = [id.strip() for id in ids_to_remove if id.strip()]

    st.button("Restore Original file", on_click=restore_original_file_callback)

    if not df.empty and st.button("Remove Tasks"):
        filtered_df = remove_tasks(df, ids_to_remove, id_key)
        jsonl_data = filtered_df.to_json(orient="records", lines=True)

        data_preview_fragment(filtered_df)

        download_fragment(filtered_df, jsonl_data)


if __name__ == "__main__":
    main()
