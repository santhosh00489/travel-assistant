'''import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("CDM Info Hub")

question = st.text_input("QUESTION: ")
if st.button("Enter"):
if question:
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    st.header("ANSWER")
    st.write(response)'''
'''import streamlit as st
from langchain_helper import get_few_shot_db_chain

st.title("CDM Info Hub")

question = st.text_input("QUESTION: ")

if st.button("Enter"):
    if question:
        chain = get_few_shot_db_chain()
        response = chain.run(question)

        st.header("ANSWER")
        st.write(response)'''

import streamlit as st
from langchain_helper import get_few_shot_db_chain

# Set page title and favicon
st.set_page_config(page_title="CDM Info Hub", page_icon="🌐")

# Define app layout using the new Streamlit columns feature
st.title("Chidam Info Hub")

# Create a two-column layout
question_col, answer_col = st.beta_columns([2, 1])

# Add a sidebar for additional information or settings
with st.sidebar:
    st.subheader("Settings")
    # Add any additional settings or information here

# Input for user question
question = question_col.text_input("Ask a question:", key="question_input")

# Button to trigger the response
if question_col.button("Get Answer", key="enter_button"):
    if question:
        # Fetch response from the language chain
        chain = get_few_shot_db_chain()
        response = chain.run(question)

        # Display the answer in the second column
        answer_col.subheader("Answer:")
        answer_col.write(response)

# Add some modern styling
question_col.image("https://example.com/your-logo.png", use_container_width=True)
question_col.markdown(
    "Welcome to the Chidam Info Hub! Ask a question about theaters, schools, shops, or hospitals."
)

# You can customize the appearance further using Streamlit's theming options and CSS styling
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

