import streamlit as st
import pandas as pd
import re
from sympy import sympify
from sympy.parsing.latex import parse_latex


def validate_text(text):
    if not text:
        return False, False, "No text to validate"

    try:
        # Define inline LaTeX delimiters patterns
        INLINE_DELIMITERS = [(r"^\$", r"\$$"), (r"^\\\(", r"\\\)$")]

        # Remove inline latex delimiters if present
        text = text.strip()
        for start_pattern, end_pattern in INLINE_DELIMITERS:
            if re.match(start_pattern, text) and re.search(end_pattern, text):
                text = re.sub(start_pattern, "", text)
                text = re.sub(end_pattern, "", text)
                break

        parsed = parse_latex(text, strict=True)
        value = sympify(parsed)
        return True, value.is_number, ""
    except Exception as e:
        return False, False, str(e)


st.title("Remove IDs from export")


uploaded_file = st.file_uploader("Choose a JSONL file", type="jsonl")
id_key = st.text_input("ID key", value="idx")
category_key = st.text_input("Category key", value="metadata.sub_category")
to_validate_key = st.text_input("Verification key (Latex)", value="verification")

df = None
original_df = None
if uploaded_file is not None:
    df = pd.read_json(uploaded_file, lines=True)
    original_df = df.copy()

col1, col2 = st.columns(2)
with col1:
    st.header("IDs to Remove")
    ids_to_remove_text = st.text_area("IDs to Remove", value="", key="ids_to_remove")

    if st.button("Remove IDs", key="remove_ids"):
        if df is not None:
            # Extract alphanumeric strings with length > 10
            ids_to_remove = re.findall(r"[a-zA-Z0-9-]{10,}", ids_to_remove_text)

            if ids_to_remove:
                # Filter out rows with matching IDs
                df = df[~df[id_key].isin(ids_to_remove)]
                st.toast(f"Removed {len(ids_to_remove)} IDs")
                st.write(f"Found and removed {len(ids_to_remove)} IDs")
            else:
                st.toast("No valid IDs found to remove")

with col2:
    st.header("IDs to add")
    ids_to_add_text = st.text_area("IDs to add", value="", key="ids_to_add")

    if st.button("Add IDs", key="add_ids"):
        if original_df is not None:
            # Extract alphanumeric strings with length > 10
            ids_to_add = re.findall(r"[a-zA-Z0-9]{10,}", ids_to_add_text)

            if ids_to_add:
                # Find rows in original_df that match the IDs and aren't already in df
                rows_to_add = original_df[original_df[id_key].isin(ids_to_add)]
                # Only add rows that aren't already in the current df
                rows_to_add = rows_to_add[~rows_to_add[id_key].isin(df[id_key])]

                if not rows_to_add.empty:
                    df = pd.concat([df, rows_to_add], ignore_index=False)
                    st.toast(f"Added {len(rows_to_add)} IDs back to the dataset")
                    st.write(f"Found and added {len(rows_to_add)} IDs")
                else:
                    st.toast("No new IDs to add")
            else:
                st.toast("No valid IDs found to add")


if df is not None:
    # Display the data editor
    st.header("All Data")
    edited_df = st.data_editor(df)

    # Display number of unique items per category
    st.header("Category Statistics")
    # Extract the category from nested JSON if needed
    if "." in category_key:
        parts = category_key.split(".")
        category_values = df[parts[0]].apply(
            lambda x: x.get(parts[1]) if isinstance(x, dict) else None
        )
    else:
        category_values = df[category_key]

    # Count unique items per category
    category_counts = category_values.value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]

    # Add a total row
    total_row = pd.DataFrame({"Category": ["All"], "Count": [len(df)]})
    category_counts = pd.concat([category_counts, total_row], ignore_index=True)

    # Display as a bar chart (excluding the "All" category)
    st.bar_chart(
        category_counts[category_counts["Category"] != "All"].set_index("Category")
    )

    # Create a dataframe for display with download buttons
    display_df = category_counts.copy()
    display_df["Download"] = None  # Placeholder column for buttons

    # Display the table with the statistics and download buttons
    st.write(f"Number of unique items per {category_key}:")

    # Create columns for the table: Category, Count, Download
    cols = st.columns([3, 1, 2])
    cols[0].write("**Category**")
    cols[1].write("**Count**")
    cols[2].write("**Download**")

    # Display each row with a download button
    for idx, row in display_df.iterrows():
        category = row["Category"]
        count = row["Count"]

        # Create columns for each row
        cols = st.columns([3, 1, 2])
        cols[0].write(category)
        cols[1].write(count)

        # Filter data for this category
        if category == "All":
            filtered_data = df
        else:
            if "." in category_key:
                parts = category_key.split(".")
                filtered_data = df[
                    df[parts[0]].apply(
                        lambda x: (
                            x.get(parts[1]) == category
                            if isinstance(x, dict)
                            else False
                        )
                    )
                ]
            else:
                filtered_data = df[df[category_key] == category]

        # Convert to JSONL for download
        jsonl_data = filtered_data.to_json(orient="records", lines=True)

        # Create download button
        download_filename = f"{category.replace(' ', '_').lower()}_items.jsonl"
        cols[2].download_button(
            label=f"Download {category} items",
            data=jsonl_data,
            file_name=download_filename,
            mime="application/jsonl",
            key=f"download_{idx}",
        )


if df is not None:

    # Add validation table
    st.header("Validation Results")

    # Create validation results
    validation_results = []
    for _, row in df.iterrows():
        id_value = row[id_key]

        # Extract the validation text based on to_validate_key
        if "." in to_validate_key:
            parts = to_validate_key.split(".")
            to_validate = (
                row[parts[0]].get(parts[1]) if isinstance(row[parts[0]], dict) else None
            )
        else:
            to_validate = row.get(to_validate_key, "")

        # Validate the text
        is_valid, is_number, error = validate_text(to_validate)

        validation_results.append(
            {
                "ID": id_value,
                "Value": to_validate,
                "Is LaTeX": is_valid,
                "Is Number": is_number,
                "Error": error,
            }
        )

    # Create validation dataframe
    validation_df = pd.DataFrame(validation_results)

    # Display validation table
    st.dataframe(validation_df)

    # Display validation summary
    st.subheader("Validation Summary")
    total_count = len(validation_df)
    valid_latex_count = validation_df["Is LaTeX"].sum()
    number_count = validation_df["Is Number"].sum()

    summary_data = {
        "Metric": ["Total Items", "Valid LaTeX", "Numbers"],
        "Count": [total_count, valid_latex_count, number_count],
        "Percentage": [
            "100%",
            f"{valid_latex_count/total_count*100:.1f}%" if total_count > 0 else "0%",
            f"{number_count/total_count*100:.1f}%" if total_count > 0 else "0%",
        ],
    }

    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)
