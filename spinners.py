import streamlit as st
import time
import asyncio 

st.title("Long running tasks")

with st.spinner("Processing..."):
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i+1)

st.success("Done! Task completed.")

st.title("Async Example")

async def async_task():
    for i in range(5):
        st.write(f"Async step {i + 1}")
        await asyncio.sleep(1)
asyncio.run(async_task())

st.success("Async task done!")

st.title("Queue based background tasks")
@st.cache_resource
def expensive_task(x):
    time.sleep(5)
    return f"Result for input{x}"

input_val = st.text_input("Enter something")

if st.button("run task"):
    with st.spinner("Running task in queue"):
        result = expensive_task(input_val)
    st.success(result)