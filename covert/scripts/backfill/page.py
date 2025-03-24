from covert.common.file_uploader import file_uploader
from covert.states.file_state import FileState
import streamlit as st
import uuid


class Condition:
    def __init__(self, value: str):
        self.value = value
        self.id = str(uuid.uuid4())


def main():
    st.title("Backfill")
    st.text("Backfill data from one file to another")
    st.divider()

    uploaded_file = file_uploader()

    if uploaded_file:
        st.write("yay")

    if st.button("Login"):
        st.login()

    if "conditions" not in st.session_state:
        conditions = []
    else:
        conditions = st.session_state["conditions"]

    def delete_condition(condition: Condition):
        conditions.remove(condition)
        st.session_state["conditions"] = [*conditions]

    def add_condition():
        conditions.append(Condition("emma"))
        st.session_state["conditions"] = [*conditions]

    for index, condition in enumerate(conditions):
        with st.container(height=150):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.text_input(f"Condition", value=condition.value, key=condition.id)
            with col2:
                st.button(
                    "Delete",
                    key=f"delete_{condition.id}",
                    on_click=delete_condition,
                    args=[condition],
                )
            with col3:
                st.write(len(conditions))
                st.button("Move Up", key=f"move_up_{condition.id}")
    st.button("Add", on_click=add_condition)
    if st.button("Save"):
        st.session_state["conditions"] = [*conditions]

    st.write(conditions)
