import streamlit as st
import pandas as pd

from covert.common.data_preview import data_preview
from covert.common.upload_file import upload_file
from covert.common.download_url import download_from_url
from covert.scripts.types.parse_type import ParseType
from covert.utils.dataframes import get_keys
from covert.utils.latex import extract_all_text, extract_math_expressions, validate_text


@st.fragment
def latex_expression_editor(
    expression, error_msg, key_prefix, parse_type: ParseType = ParseType.SYMPY_ANTLR
):
    """Fragment to edit and validate a single LaTeX expression."""
    # Display the original expression
    st.code(expression, language="latex")

    # Create editable textarea with the expression
    edited_expr = st.text_area(
        "Edit LaTeX expression:",
        value=expression,
        key=f"textarea_{key_prefix}",
        height=100,
    )

    # Show current rendering
    st.latex(edited_expr)

    # Show original error
    st.error(error_msg)

    # Add validation button
    if st.button("Validate edited expression", key=f"validate_{key_prefix}"):
        is_valid, _, new_error_msg = validate_text(edited_expr, parse_type)
        if is_valid:
            st.success("LaTeX expression is now valid!")
        else:
            st.error(f"Still invalid: {new_error_msg}")


@st.fragment
def preview_errors(errors, parse_type: ParseType = ParseType.SYMPY_ANTLR):
    """Display paginated error results with expandable details"""
    if not errors:
        st.info("No errors found!")
        return

    # Pagination controls
    items_per_page = 10
    total_pages = (len(errors) + items_per_page - 1) // items_per_page

    page = st.session_state.get("error_page", 1)

    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(errors))

    # Display paginated results
    for index, item in enumerate(errors[start_idx:end_idx]):
        with st.expander(f"ID: {item['id']} - {item['error_count']} errors"):
            for i, error in enumerate(item["faulty_expressions"]):
                st.markdown(f"**Error {i + 1}:**")
                latex_expression_editor(
                    error["expression"],
                    error["error"],
                    f"error_{index}_{i}",
                    parse_type,
                )
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        page = st.number_input(
            "Page", min_value=1, max_value=total_pages, value=1, key="error_page"
        )

    csv_data = []
    for item in errors:
        for expr in item["faulty_expressions"]:
            csv_data.append(
                {
                    "id": item["id"],
                    "expression": expr["expression"],
                    "error": expr["error"],
                }
            )

    if csv_data:
        df_errors = pd.DataFrame(csv_data)
        csv = df_errors.to_csv(index=False)
        st.download_button(
            label="Download errors as CSV",
            data=csv,
            file_name="latex_errors.csv",
            mime="text/csv",
        )


def get_errors(df, id_key, validation_keys, parse_type):
    """
    Validate LaTeX expressions in the dataframe and return errors.
    Supports nested keys using dot notation (e.g., "parent.child").

    Args:
        df: pandas DataFrame containing the data
        id_key: column name for the ID field
        validation_keys: list of column names to validate (empty means validate all)
        parse_type: ParseType enum value indicating how to parse the expressions

    Returns:
        list of dicts containing error information for each row with invalid LaTeX
    """
    results = []

    def get_nested_value(row, key):
        """Helper function to get value from nested dictionary using dot notation"""
        if "." in key:
            parent_key, child_key = key.split(".", 1)
            if isinstance(row[parent_key], dict):
                return row[parent_key].get(child_key, "")
        return row[key]

    for _, row in df.iterrows():
        # Get row ID using nested key if necessary
        row_id = get_nested_value(row, id_key)

        # If validation_keys is empty, validate all text in the row
        if not validation_keys:
            text = extract_all_text(row.to_dict())
        else:
            # Combine text from specified columns, handling nested keys
            texts = [get_nested_value(row, key) for key in validation_keys]
            text = extract_all_text(texts)

        expressions = extract_math_expressions(text)

        # Validate each expression
        faulty_expressions = []
        for expr in expressions:
            is_valid, _, error_msg = validate_text(expr, parse_type)
            if not is_valid:
                faulty_expressions.append({"expression": expr, "error": error_msg})

        # Add to results if there are faulty expressions
        if faulty_expressions:
            results.append(
                {
                    "id": row_id,
                    "error_count": len(faulty_expressions),
                    "faulty_expressions": faulty_expressions,
                }
            )

    return results


def main():
    st.title("Latex Validator")

    # generate a helper text here
    st.markdown("")

    upload_file("Choose a file (JSONL)")
    download_from_url("Download from URL (optional)", "Download from URL")

    st.divider()

    df = st.session_state.df

    data_preview(df)

    keys = get_keys(df)

    id_key = st.selectbox("ID Key", keys)

    validation_keys = st.multiselect(
        "Select keys to validate (Leave empty to validate all)", keys
    )

    parse_type = st.selectbox("Parse Type", ParseType)

    if st.button("Validate"):
        errors = get_errors(df, id_key, validation_keys, parse_type)
        st.write(f"Errors: {len(errors)}/{len(df)}")
        preview_errors(errors, parse_type)


if __name__ == "__main__":
    main()
