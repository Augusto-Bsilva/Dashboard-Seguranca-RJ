import streamlit as st
import pandas as pd

data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
    "City": ["New York", "Los Angeles", "Chicago", "Houston"]
}

df = pd.DataFrame(data)

st.write("### Using `st.write()` to display a DataFrame")
st.write(df)

st.write("Static Table")
st.table(df)

st.write("Interactive DataFrame with `st.dataframe()`")
st.dataframe(df)

person = {
    "Name": "Eve",
    "Age": 28,
    "Skills": ["Python", "Data Analysis", "Machine Learning"]
}
st.json(person)
st.write("### JSON Example", person)

editable_df = st.data_editor(df,num_rows="dynamic")
st.write("Updated DataFrame")
st.write(editable_df)

with st.container():
    st.write("This is inside a container.")

col1, col2 = st.columns(2)

with col1:
    st.write("Col1 content")
with col2:
    st.write("Col2 content")

with st.expander("Click to expand"):
    st.write("Hidden content inside the expander.")

option = st.sidebar.selectbox("Select page:", ["Home", "Settings", "About"])

st.sidebar.write("Sidebar content here")
st.sidebar.write(f"You selected: {option}")

st.divider()
st.caption("This is a caption text. It can be used to provide additional context or information.")