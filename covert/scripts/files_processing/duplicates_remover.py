from pydantic import BaseModel
import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value
from covert.utils.files import get_df


class ReferenceFile(BaseModel):
    df: pd.DataFrame
    unique_key: str | None = None
    name: str
    duplicates: set[str] = set()

    model_config = {"arbitrary_types_allowed": True}


def append_file(file: ReferenceFile, unique_key: str):
    files = st.session_state.files
    file.unique_key = unique_key
    files.append(file)
    st.session_state.files = files


def upload_callback(session_key: str):
    uploaded_file = st.session_state[session_key]
    if not uploaded_file:
        return
    file_name = uploaded_file.name
    df = get_df(uploaded_file.getvalue(), file_name)
    st.session_state.chosen_file = ReferenceFile(df=df, name=file_name)


def main():
    st.title("Remove duplicates from file")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    unique_key_main = st.selectbox("Select Unique Key", keys)

    if "files" not in st.session_state:
        st.session_state.files = []
    if "chosen_file" not in st.session_state:
        st.session_state.chosen_file = ReferenceFile(df=pd.DataFrame(), name="")

    files: list[ReferenceFile] = st.session_state.files
    for index, file in enumerate(files):
        with st.container(border=True, height=150):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"File {index}: {file.name}")
            with col2:
                st.write(f"Unique Key: {file.unique_key}")
            with col3:
                st.write(f"Duplicates: {len(file.duplicates)}")
            with col4:
                if st.button("Delete File", key=f"delete_file_{index}"):
                    files.remove(file)
                    st.session_state.files = files
                    st.rerun()

    with st.container(height=500):
        chosen_file = st.session_state.chosen_file
        uploaded_file = st.file_uploader(
            "Choose a file (JSONL)",
            key=f"duplicates_remover_upload",
            on_change=upload_callback,
            args=("duplicates_remover_upload",),
        )
        url_input = st.text_input(
            "Download from URL (optional)", key=f"duplicates_remover_url"
        )
        st.button("Download from URL", args=(url_input, "duplicates_remover_button"))
        keys = get_keys(chosen_file.df)

        if not chosen_file.df.empty:
            unique_key = st.selectbox(
                "Select Unique Key", keys, key=f"duplicates_remover_unique_key"
            )
            st.button(
                "Add file",
                on_click=append_file,
                args=(chosen_file, unique_key),
            )

    if st.button("Find duplicates"):
        if not unique_key_main:
            st.error("Please select a unique key for the main file")
            return

        # Get values from main dataframe
        main_values = set(
            df.apply(
                lambda row: get_nested_value(row.to_dict(), unique_key_main), axis=1
            )
        )
        duplicates_found = False

        # Check against each reference file
        for file in files:
            if not file.unique_key:
                st.error(f"No unique key selected for reference file: {file.name}")
                continue

            # Find values that exist in both dataframes
            ref_values = set(
                file.df.apply(
                    lambda row: get_nested_value(row.to_dict(), file.unique_key), axis=1
                )
            )
            duplicates = main_values.intersection(ref_values)

            if duplicates:
                duplicates_found = True
                file.duplicates = duplicates

        if not duplicates_found:
            st.success("No duplicates found in any reference file!")
        st.session_state.files = files
        st.rerun()

    if st.button("Remove duplicates"):
        if not unique_key_main:
            st.error("Please select a unique key for the main file")
            return

        # Collect all duplicate values from reference files
        all_duplicates = set()
        for file in files:
            all_duplicates.update(file.duplicates)

        if not all_duplicates:
            st.info("No duplicates to remove")
            return

        # Remove rows where the unique key value is in any of the duplicates sets
        mask = ~df.apply(
            lambda row: get_nested_value(row.to_dict(), unique_key_main)
            in all_duplicates,
            axis=1,
        )
        st.session_state.df = df[mask]
        st.success(f"Removed {len(all_duplicates)} duplicate values")
        st.rerun()


if __name__ == "__main__":
    main()
