from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

llm = HuggingFaceEndpoint(
        repo_id="moonshotai/Kimi-K3",
        task="text-generation"
)

st.header("Research Tool")

user_input = st.text_input("Enter your prompt")

if st.button:
    st.text("Some random text")