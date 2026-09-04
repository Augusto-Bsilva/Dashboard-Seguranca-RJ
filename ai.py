import os 
import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory

st.title("AI Chat Assistant")

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

if "chain" not in st.session_state:
    llm = ChatGroq(model_name="gpt-4o-mini", temperature=0.7)
    st.session_state.chain = ConversationChain(llm=llm, memory = st.session_state.memory)

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:",key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    response = st.session_state.chain.run(user_input)
    st.session_state.last.response = response

if st.session_state.memory.buffer:
    st.markdown("###Conversation History")
    for line in st.session_state.memory.buffer.strip().split("\n"):
        if line.strip():
            st.write(line)
