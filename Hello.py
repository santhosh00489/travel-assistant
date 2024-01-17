import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("CDM Info Hub")

question = st.text_input("QUESTION: ")

if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    st.header("ANSWER")
    st.write(response)
