import jsonata.jsonata
import streamlit as st
import jsonata
import pandas as pd
import csv
import io
import base64


@st.fragment
def gencsv():
    row_schema = st.text_area("Row Schema", value="")

    # Add a button to transform data using JSONata
    if st.button("Transform Data"):
        if "df" in st.session_state:
            # Get the JSONata expression from row_schema
            try:
                expression = jsonata.Jsonata(row_schema)

                # Create a list to store transformed rows
                transformed_rows = []

                # Apply JSONata transformation to each row in the dataframe
                for _, row in st.session_state["df"].iterrows():
                    # Convert row to dict for JSONata processing
                    row_dict = row.to_dict()
                    # Apply transformation
                    transformed_row = expression.evaluate(row_dict)
                    transformed_rows.append(transformed_row)

                # Store transformed rows in session state
                st.session_state["transformed_rows"] = transformed_rows

                # Display success message
                st.success(
                    f"Successfully transformed {len(transformed_rows)} rows using JSONata"
                )

                # Display preview of transformed data
                st.write("Preview of transformed data:")
                preview_df = pd.DataFrame(transformed_rows)
                st.dataframe(
                    preview_df.head(5) if len(transformed_rows) > 5 else preview_df
                )

            except Exception as e:
                st.error(f"Error transforming data: {str(e)}")
        else:
            st.warning("No data available. Please upload a file first.")

    # Add a download button for CSV
    if (
        "transformed_rows" in st.session_state
        and len(st.session_state["transformed_rows"]) > 0
    ):
        # Create CSV from transformed rows
        def convert_to_csv(transformed_rows):
            # Get all keys from all dictionaries to ensure all columns are included
            all_keys = set()
            for row in transformed_rows:
                all_keys.update(row.keys())

            fieldnames = list(all_keys)

            # Create CSV in memory
            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transformed_rows)

            return csv_buffer.getvalue()

        # Generate CSV data
        csv_data = convert_to_csv(st.session_state["transformed_rows"])

        # Display download button
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="transformed_data.csv",
            mime="text/csv",
        )
