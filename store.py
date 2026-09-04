import streamlit as st

st.title("Session State Demo")

if "counter" not in st.session_state:
    st.session_state.counter = 0
if st.button ("Increment"):
    st.session_state.counter += 1

st.write("Counter value:", st.session_state.counter)

if "name" not in st.session_state:
    st.session_state.name = "Guest"

name_input = st.text_input("Enter in your name", st.session_state.name)
if name_input != st.session_state.name:
    st.session_state.name = name_input

st.write("Hello", st.session_state.name)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    if st.button("Login"):
        st.session_state.logged_in = True
        st.success("You are now logged in!")

else:
    st.write("Welcome back!")
    if st.button("Logout"):
             st.session_state.logged_in = False