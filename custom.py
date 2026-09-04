import streamlit as st

st.title("Custom Theme Example")

st.markdown("""
    <style>
    .ccc-1aumxhk{
        background-color: #f0f0f0;
    }
    .stButton>button {
    background-color: #4CAF50;
    color:white; 
    }
    </style>
""",
    unsafe_allow_html=True
)

st.button("Styled Button")