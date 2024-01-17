'''import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("ChidambaramLocator")

question = st.text_input("Question: ")

if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    st.header("Answer")
    st.write(response)'''
import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.beta_set_page_config(layout="wide")
hide_menu_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_menu_style, unsafe_allow_html=True)

col1, col2 = st.columns((1, 2))

with col1:
    st.image('logo.png', width=300)

with col2:
    st.title("📍 Chidambaram Locator")

question = st.text_area("Type your question here...", height=100)

if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    with st.expander("See the SQL query used"):
        st.write(chain.sql_query)

    with st.container():
        st.header("Answer")
        st.success(response)
