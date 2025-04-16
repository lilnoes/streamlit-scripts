import jsonata
import streamlit as st


def transform_data(data: list[dict], schema: str) -> list[str]:
    try:
        expression = jsonata.Jsonata(schema)
        transformed_data = []
        for row in data:
            transformed_row = expression.evaluate(row)
            transformed_data.append(transformed_row)
        return transformed_data
    except Exception as e:
        st.error(f"Error transforming data: {str(e)}")
    return []
