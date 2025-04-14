from collections import Counter
from pydantic import BaseModel
import streamlit as st
import pandas as pd
from itertools import chain

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.utils.dataframes import get_keys, get_nested_value


class CountDiff(BaseModel):
    lhs_count: int
    rhs_count: int


class DiffResult(BaseModel):
    common: dict[str, CountDiff]
    lhs_unique: list
    rhs_unique: list

    @property
    def lhs_common_values(self) -> list:
        """Returns a list of all common values from lhs (including duplicates)"""
        result = []
        for k, v in self.common.items():
            result.extend([k] * v.lhs_count)
        return result

    @property
    def rhs_common_values(self) -> list:
        """Returns a list of all common values from rhs (including duplicates)"""
        result = []
        for k, v in self.common.items():
            result.extend([k] * v.rhs_count)
        return result


def compare_dataframes(
    lhs: pd.DataFrame, rhs: pd.DataFrame, key1: str, key2: str
) -> DiffResult:
    """
    Compare values between two dataframes based on specified keys with improved efficiency.

    Args:
        df1: First dataframe
        df2: Second dataframe
        key1: Key to extract from first dataframe
        key2: Key to extract from second dataframe

    Returns:
        DiffResult containing comparison results
    """
    # Extract values efficiently
    lhs_values = [get_nested_value(item, key1) for item in lhs.to_dict("records")]
    rhs_values = [get_nested_value(item, key2) for item in rhs.to_dict("records")]

    # Use Counter for efficient counting
    lhs_counter = Counter(lhs_values)
    rhs_counter = Counter(rhs_values)

    # Find unique and common values
    unique_to_lhs = list(
        chain.from_iterable(
            [[k] * v for k, v in lhs_counter.items() if k not in rhs_counter]
        )
    )
    unique_to_rhs = list(
        chain.from_iterable(
            [[k] * v for k, v in rhs_counter.items() if k not in lhs_counter]
        )
    )

    common_values = {
        k: CountDiff(lhs_count=lhs_counter.get(k, 0), rhs_count=rhs_counter.get(k, 0))
        for k in set(lhs_counter.keys()) & set(rhs_counter.keys())
    }

    return DiffResult(
        common=common_values,
        lhs_unique=unique_to_lhs,
        rhs_unique=unique_to_rhs,
    )


@st.fragment
def diff_files_fragment(diff_result: DiffResult):
    unique_to_file1 = diff_result.lhs_unique
    with st.expander(f"Unique to File 1 ({len(unique_to_file1)} unique values)"):
        st.code(unique_to_file1)

    unique_to_file2 = diff_result.rhs_unique
    with st.expander(f"Unique to File 2 ({len(unique_to_file2)} unique values)"):
        st.code(unique_to_file2)

    with st.expander(
        f"File 1 Common values ({len(diff_result.lhs_common_values)} common values)"
    ):
        st.code(diff_result.lhs_common_values)

    with st.expander(
        f"File 2 Common values ({len(diff_result.rhs_common_values)} common values)"
    ):
        st.code(diff_result.rhs_common_values)


def data_preview_fragment(name: str, df: pd.DataFrame):
    data_preview(df, prefix_key=f"diff_files_{name}", title=f"Preview of {name} data")


def main():
    st.title("Diff files")

    # generate a helper text here
    st.markdown("""
    """)

    with st.expander("File 1"):
        upload_file("Choose a file (JSONL)", "df1", "upload_file_1")
        download_from_url(
            "Download from URL (optional)",
            "Download from URL",
            "df1",
            "download_file_1",
        )

    with st.expander("File 2"):
        upload_file("Choose a file (JSONL)", "df2", "upload_file_2")
        download_from_url(
            "Download from URL (optional)",
            "Download from URL",
            "df2",
            "download_file_2",
        )

    if "df1" not in st.session_state or "df2" not in st.session_state:
        st.warning("Please upload both files")
        st.stop()

    df1 = st.session_state.df1
    df2 = st.session_state.df2

    file1_keys = get_keys(df1)
    file2_keys = get_keys(df2)

    file1_key = st.selectbox("Select a key from File 1", file1_keys)
    file2_key = st.selectbox("Select a key from File 2", file2_keys)

    data_preview_fragment("File 1", df1)
    data_preview_fragment("File 2", df2)

    st.divider()

    if st.button("Compare files"):
        diff_result = compare_dataframes(df1, df2, file1_key, file2_key)
        diff_files_fragment(diff_result)


if __name__ == "__main__":
    main()
