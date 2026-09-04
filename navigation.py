import streamlit as st

pages = ["Home", "Dashboard", "Settings"]
choice = st.sidebar.radio("Go to", pages)

if choice == "Home":
    st.header("home page")
    st.write("Welcome to the Home page! Here you can find an overview of the application and its features.")
elif choice == "Dashboard":
    st.header("dashboard page")
    st.write("metrics and charts here")
elif choice == "Settings":
    st.header("settings page")
    st.write("user preferences here")