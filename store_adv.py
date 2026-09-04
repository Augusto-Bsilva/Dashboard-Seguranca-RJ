import streamlit as st

st.title("Advanced Session State Demo")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

if st.button("Reset"):
    st.session_state.count = 0


st.write(f"Current Count: {st.session_state.count}")