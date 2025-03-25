import re
import streamlit as st
import json

from utils import validate_text, extract_math_expressions, extract_all_text


@st.fragment
def latex_expression_editor(expression, error_msg, key_prefix):
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
        is_valid, _, new_error_msg = validate_text(edited_expr)
        if is_valid:
            st.success("LaTeX expression is now valid!")
        else:
            st.error(f"Still invalid: {new_error_msg}")


@st.fragment
def latexall():
    col1, col2 = st.columns(2)
    with col1:
        is_all = st.checkbox("Validate All keys", value=False)
    with col2:
        if not st.button("Validate Latex"):
            return
    if "df" not in st.session_state:
        st.error("No data to validate")
        return
    df = st.session_state["df"]
    to_validate_key = st.session_state["to_validate_key"]
    id_key = st.session_state["id_key"]
    if id_key not in df.columns:
        st.error(f"ID Column {id_key} not found in data")
        return
    if to_validate_key not in df.columns and not is_all:
        st.error(f"Verification Column {to_validate_key} not found in data")
        return

    # Extract expressions and validate them
    results = []
    faulty_ids_count = 0

    for _, row in df.iterrows():
        row_id = row[id_key]
        if is_all:
            text = extract_all_text(row.to_dict())
        else:
            text = row[to_validate_key]
            text = extract_all_text(text)
        expressions = extract_math_expressions(text)

        # Validate each expression
        faulty_expressions = []
        for expr in expressions:
            is_valid, _, error_msg = validate_text(expr)
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
            faulty_ids_count += 1

    # Display results
    if results:
        st.write(f"Found {faulty_ids_count}/{len(df)} IDs with LaTeX errors:")

        for result in results:
            with st.expander(f"ID: {result['id']} - {result['error_count']} errors"):
                for i, expr in enumerate(result["faulty_expressions"]):
                    st.markdown(f"**Error {i+1}:**")
                    expr_key = f"expr_{result['id']}_{i}"

                    # Use a fragment for each expression editor
                    latex_expression_editor(expr["expression"], expr["error"], expr_key)
    else:
        st.success("No LaTeX errors found!")
