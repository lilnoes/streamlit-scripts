import streamlit as st


def data_preview(df, page_size=50, prefix_key=""):
    if df.empty:
        return
    page_key = f"{prefix_key}_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
        page = 0
    else:
        page = st.session_state[page_key]

    # Calculate total pages and row information
    total_rows = len(df)
    total_pages = (total_rows - 1) // page_size
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_rows)

    with st.expander("Data Preview"):

        # Display the dataframe slice for current page
        st.dataframe(df.iloc[start_idx:end_idx])

        # Display pagination controls below the dataframe
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.button(
                "← Previous",
                disabled=(page <= 0),
                on_click=lambda: setattr(st.session_state, page_key, page - 1),
                key=f"{prefix_key}_previous",
            )

        with col2:
            st.write(
                f"Page {page + 1} of {total_pages + 1} (Rows {start_idx + 1}-{end_idx} of {total_rows})"
            )

        with col3:
            st.button(
                "Next →",
                disabled=(page >= total_pages),
                on_click=lambda: setattr(st.session_state, page_key, page + 1),
                key=f"{prefix_key}_next",
            )
