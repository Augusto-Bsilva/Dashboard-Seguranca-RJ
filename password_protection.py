import streamlit as st

password_input = st.text_input("Enter Password", type="password")

if password_input == st.secrets["auth"]["password"]:
    st.success("Access Granted")
    st.write("Protected Content in Here")
else:
    st.warning("Enter in the correctPassword!!!")