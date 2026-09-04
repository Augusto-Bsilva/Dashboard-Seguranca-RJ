import streamlit as st

st.title("Multi Tab Example")

tabs = st.tabs(["Sumary", "Details", "Settings"])

with tabs[0]:
    st.header("Summary")
    st.write("Overview Content Here")
with tabs[1]:
    st.header("Details")
    st.write("Detailed info goes Here")
with tabs[2]:
    st.header("Settings")
    st.write("User Preferences Here")