import streamlit as st

def show_header(title):
    st.markdown(f'## {title}')

def show_metric(label,value):
    st.metric(label=label, value=value)

show_header("Dashboard")
show_metric("Revenue", "$10,000")
show_metric("Users", "1,000")