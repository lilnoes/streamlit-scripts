import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value


def split_tasks(df: pd.DataFrame, split_key: str) -> tuple[dict, dict]:
    # Group data by the key value (nested or direct)
    grouped_data = {}
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        category = get_nested_value(row_dict, split_key)
        if category not in grouped_data:
            grouped_data[category] = []
        grouped_data[category] = grouped_data[category] + [row_dict]

    # Convert each group to JSONL format and count items
    jsonl_data = {}
    counts = {}
    for category, data in grouped_data.items():
        category_df = pd.DataFrame(data)
        jsonl_data[category] = category_df.to_json(orient="records", lines=True)
        counts[category] = len(category_df)

    # Add "All" category
    jsonl_data["All"] = df.to_json(orient="records", lines=True)
    counts["All"] = len(df)

    return jsonl_data, counts


def main():
    st.title("Split Tasks By Key")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    split_key = st.selectbox("Select Key", keys)

    if st.button("Split Tasks"):
        split_data, category_counts = split_tasks(df, split_key)

        st.header("Download Split Files")

        # Create column headers
        cols = st.columns([3, 1, 2])
        cols[0].write("**Category**")
        cols[1].write("**Count**")
        cols[2].write("**Download**")

        # Display each category row
        for category in split_data.keys():
            cols = st.columns([3, 1, 2])
            category_name = str(category) if category is not None else "none"

            # Display category name
            cols[0].write(category_name)

            # Display count
            cols[1].write(category_counts[category])

            # Add download button
            download_filename = f"{category_name.replace(' ', '_').lower()}_items.jsonl"
            cols[2].download_button(
                label=f"Download {category_name}",
                data=split_data[category],
                file_name=download_filename,
                mime="application/jsonl",
                key=f"download_{category_name}",
            )


if __name__ == "__main__":
    main()
