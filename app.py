import streamlit as st

st.title("Re-execution demo")
st.header("Welcome to My Streamlit App")
st.subheader("This is a subheader")

st.markdown("This is a markdown text. You can use **bold**, *italic*, and other formatting options.")

st.text("This is a simple text element. You can use it to display plain text.")
st.write("`st.write()` can handle *mixed content* like this **bold**, _italic_, and numbers:",123)


st.markdown("### Code Block Example")
st.code("""
#Python Example
def greet(name):
    return f"Hello, {name}!"
print(greet("Streamlit"))
""",language="python")

st.markdown("### Inline LaTeX: $a^2 + b^2 = c^2$")
st.latex(r"\int_{a}^{b} x^2 dx")

st.success("This is a success message!")
st.info("This is an info message.")
st.warning("This is a warning message!")
st.error("This is an error message.")
st.markdown("> **Tip:** Use feedback messages to guide the user")

if st.button("Click me!"):
    st.write("Button clicked!")

choice = st.radio("Choose an option:", ["Option 1", "Option 2", "Option 3"])
st.write("You selected:",choice)

agree = st.checkbox("I agree to the terms and conditions")
if agree:
    st.write("Thank you for agreeing!")

genre = st.selectbox("Pick a genre:",["Metal", "Rock", "Bluerock"])
st.write("You selected:", genre)

metal_subgenre = st.multiselect("Pick a metal subgenre:",["Black Metal", "Death Metal", "Power Metal"])
st.write("You selected:", metal_subgenre)


age = st.slider("Select your age:", 0, 100, 25)
st.write("You selected:", age)

number = st.number_input("Enter a number:", min_value=0, max_value=100, value=10)
st.write("You entered:", number)

name = st.text_input("Enter your name")
st.write("Hello,", name)

bio = st.text_area("Enter a short bio")
st.write("Your bio:", bio)

date = st.date_input("Pick a date")
st.write("You selected:", date)

time = st.time_input("Pick a time")
st.write("You selected:", time)

uploaded_file = st.file_uploader("Upload a text file",type = ["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode('utf-8')
    st.text_area("File content:",content,height=200)