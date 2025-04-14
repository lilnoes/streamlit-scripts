import streamlit as st


def data_previewer(
    total_size,
    get_page_data,
    page_size=50,
    prefix_key="",
    title="Data Preview",
    render_fn=st.dataframe,
):
    """
    Generic data preview component with pagination

    Args:
        total_size: Total number of items
        get_page_data: Function that takes (start_idx, end_idx) and returns data for that page
        page_size: Number of items per page
        prefix_key: Prefix for session state keys
        render_fn: Function to render the data (defaults to st.dataframe)
    """
    page_key = f"{prefix_key}_page"
    if page_key not in st.session_state:
        st.session_state[page_key] = 0
        page = 0
    else:
        page = st.session_state[page_key]

    # Calculate total pages and row information
    total_pages = (total_size - 1) // page_size
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, total_size)

    with st.expander(title):
        # Get and display the data for current page
        current_page_data = get_page_data(start_idx, end_idx)
        render_fn(current_page_data)

        # Display pagination controls below the data
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
                f"Page {page + 1} of {total_pages + 1} (Items {start_idx + 1}-{end_idx} of {total_size})"
            )

        with col3:
            st.button(
                "Next →",
                disabled=(page >= total_pages),
                on_click=lambda: setattr(st.session_state, page_key, page + 1),
                key=f"{prefix_key}_next",
            )


def data_preview(df, page_size=50, prefix_key="", title="Data Preview"):
    """Legacy function that uses data_previewer for DataFrame pagination"""
    if df.empty:
        return
    return data_previewer(
        total_size=len(df),
        get_page_data=lambda start, end: df.iloc[start:end],
        page_size=page_size,
        prefix_key=prefix_key,
        title=title,
    )
