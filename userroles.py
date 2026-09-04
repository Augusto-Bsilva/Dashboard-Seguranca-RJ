import streamlit as st

if "user role" not in st.session_state:
    st.session_state.user_role = None

def login(user):
    roles = {"admin": "admin", "user": "viewer"}
    st.session_state.user_role = roles.get(user, "viewer")

user = st.text_input("Username")
if st.button("Login"):
    login(user)

if st.session_state.user_role == "admin":
    st.success("Welcome, Admin! You have full access.")
    st.write("Admin content")

elif st.session_state.user_role == "viewer":
    st.info("Welcome, Viewer! You have limited access.")
    st.write("Viewer content")
else:
    st.warning("Please login")