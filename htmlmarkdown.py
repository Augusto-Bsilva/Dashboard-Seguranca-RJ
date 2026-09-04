import streamlit as st

html_code = """
     <div style="background-color: lightblue; padding: 10px; border-radius: 5px;">
         <h2 style="color: darkblue;">Welcome to My Streamlit App</h2>
         <p>This is a simple HTML block rendered in Streamlit.</p>
     </div>
"""
st.markdown(html_code, unsafe_allow_html=True)