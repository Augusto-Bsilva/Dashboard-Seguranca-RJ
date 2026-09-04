import streamlit as st
import pandas as pd
import json

st.title("File upload and preview")

uploaded_file = st.file_uploader("Upload a CSV, Excel or JSON file", type=["csv", "xlsx", "json"])

if uploaded_file:
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
        st.write("CSV Preview")
        st.dataframe(df.head())

    elif uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)
        st.write("Excel Preview")
        st.dataframe(df.head())

    elif uploaded_file.name.endswith("json"):
        df = pd.read_json(uploaded_file)
        st.write("Json Preview")
        st.dataframe(df.head())

if uploaded_file:
    file_size = uploaded_file / 1024
    st.write(f"File name: {uploaded_file.name}, Size: {uploaded_file.size:.2f}KB")
    if file_size > 500:
        st.warning("File too large, previw may be limited")

@st.cache_data
def load_large_csv(file):
    return pd.read_csv(file)

st.write("Upload a large csv for cashing demo")
large_csv = st.file_uploader("Upload csv for cashing", type=['csv'], key=['large'])

if large_csv:
    df_large = load_large_csv(large_csv)
    st.write("Cashed CSV Loaded")
    st.dataframe(df_large.head())