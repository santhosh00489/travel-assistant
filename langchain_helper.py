from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
import streamlit as st
import subprocess
command = [
    "curl",
    "--create-dirs",
    "-o",
    f"{subprocess.os.environ['HOME']}/.postgresql/root.crt",
    "https://cockroachlabs.cloud/clusters/9d023129-84e9-4d5b-a35e-82940ea18136/cert"
]
result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)

few_shots = [
    {'Question' : "what are the Vegetarian restaurant is available",
     'SQLQuery' : "SELECT name FROM google WHERE categeory = 'Vegetarian''",
     'SQLResult': "Result of the SQL query",
     'Answer' : "Ramesh High Class Vegetarian Restaurant, Hotel SABASH veg restaurant, Adyar Ananda Bhavan - A2B, Sri Lakshmi Cafe"},
    {'Question': "how many hospital is there?",
     'SQLQuery':"SELECT count(*) FROM google WHERE categeory = 'Hospital'",
     'SQLResult': "Result of the SQL query",
     'Answer': "57"},
    {'Question': "suggest me an best School?",
     'SQLQuery':" SELECT name FROM google WHERE categeory = 'School' ORDER BY ratings DESC LIMIT 5",
     'SQLResult': "Result of the SQL query",
     'Answer': "Arul Nursery & Primary School"},
    {'Question': "what are the Movie theater are available?",
     'SQLQuery':"SELECT name FROM google WHERE categeory = 'Movie theater'",
     'SQLResult': "Result of the SQL query",
     'Answer': "Maariyappa Theater 2K, LENA CINEMAS 4K- DOLBY ATMOS, VENIVE"},

]

import os
from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    DATABASE_URL = "postgresql://santhosh:tKuDH8TNAo7IeT3xsvvAjw@ready-cub-5897.6xw.aws-ap-southeast-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
    GOOGLE_API_KEY= st.secrets['AIzaSyAQDPRxDG1K3ONyY3vMr0JbGoVftUFgCpo']

    db = SQLDatabase.from_uri(st.secrets["DATABASE_URL"],sample_rows_in_table_info=3)
    llm =  GooglePalm(google_api_key=st.secrets["GOOGLE_API_KEY"],temperature=0.1)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
        Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
        Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
        Pay attention to use only the column names you can see in the tables info below. Be careful to not query for columns that do not exist.For the rating score, use the 'ratings' column. For the establishment type, extract the first word from the 'name' column.
        To identify potential recommendations among establishments, analyze factors similar to business types, popularity levels, and other significant features.

        Use the following format:

        Question: Question here
        SQLQuery: Query to run with no pre-amble
        SQLResult: Result of the SQLQuery
        Answer: Final answer here

        No pre-amble.
        """

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return chain
