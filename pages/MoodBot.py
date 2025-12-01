import streamlit as st
st.title("Chat with Zen!")
st.write("Interact with Zen - your personal mental health support chatbot")
st.components.v1.iframe("http://127.0.0.1:7860/", height=800, scrolling=True)