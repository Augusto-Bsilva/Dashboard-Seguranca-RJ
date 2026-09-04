import streamlit as st

st.title("Forms Demo")

with st.form("contact Form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submitted = st.form_submit_button("submit")

if submitted:
    st.success(f"Thanks {name}, we will contact you at {email}")


st.title("Forms Demo V2")

with st.form("Calc_Form"):
    num1 = st.number_input("Enter first Number", step=1)
    num2 = st.number_input("Enter second Number", step=1)
    calculate = st.form_submit_button("Calculate Sum")

if calculate:
    st.success(f"Results: {num1 + num2}")

st.title("Step by Step workflow")

if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "choice" not in st.session_state:
    st.session_state.choice = ""

def next_step():
    st.session_state.step+=1

def restart():
    st.session_state.step = 1
    st.session_state.name = ""
    st.session_state.choice = ""

if st.session_state.step == 1:
    st.write("Step 1: Enter your name")
    st.text_input("Name", value= st.session_state.name, key="name")
    st.button("Next", on_click=next_step)

elif st.session_state.step == 2:
    st.write(f"Hello {st.session_state.name} Step 2: Choose your preference")
    st.radio("Choose a restaurant", ['Chipotle', 'Outback'], key='choice')
    st.button("Next", on_click=next_step)

elif st.session_state.step == 3:
    st.write(f"You selected {st.session_state.choice}")
    st.button("Restart", on_click=restart)