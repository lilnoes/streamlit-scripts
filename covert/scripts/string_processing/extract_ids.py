import streamlit as st

from covert.utils.string_utils import extract_uuid


def main():
    st.title("Extract UUIDs")

    with st.expander("Helper text"):
        st.markdown(
            """
            This script extracts the UUIDs from the given data.
            """
        )

    text = st.text_area("Enter text to extract UUIDs from")

    if st.button("Extract UUIDs"):
        uuids = extract_uuid(text)
        if len(uuids) == 0:
            st.error("No UUIDs found")
        else:
            st.success(f"Extracted {len(uuids)} UUIDs")
            st.code(uuids)


if __name__ == "__main__":
    main()
