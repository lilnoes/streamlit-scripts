import streamlit as st
import json
from pydantic import BaseModel, Field
import uuid


class Item(BaseModel):
    key: str = Field(default="")
    value: str = Field(default="")
    id: uuid.UUID = Field(default_factory=uuid.uuid4, exclude=True)


class State(BaseModel):
    items: list[Item] = Field(default_factory=list)


@st.fragment
def item_fragment(item: Item):
    col1, col2 = st.columns(2)
    with col1:
        item.key = st.text_input(
            "Key", value=item.key, key=f"{item.id}_key", label_visibility="collapsed"
        )
    with col2:
        item.value = st.text_input(
            "Value",
            value=item.value,
            key=f"{item.id}_value",
            label_visibility="collapsed",
        )


def add_item(state: State):
    state.items.append(Item())


def main():
    if "state" not in st.session_state:
        st.session_state.state = State()

    state = st.session_state.state

    st.title("Convert dictionary to JSON")

    with st.expander("Helper text"):
        st.markdown(
            """
            This script converts the given dictionary to a JSON string.
            """
        )

    container = st.container(height=500)

    with container:
        col1, col2 = st.columns(2)
        with col1:
            st.text("Key")
        with col2:
            st.text("Value")
        for item in state.items:
            item_fragment(item)
    st.button("Add item", on_click=add_item, args=[state])

    if st.button("Convert to JSON"):
        json_string = json.dumps(
            {item.key: item.value for item in state.items if item.key and item.value}
        )
        st.code(json_string)


if __name__ == "__main__":
    main()
