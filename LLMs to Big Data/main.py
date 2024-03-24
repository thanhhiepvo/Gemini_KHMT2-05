import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to DataHub! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ### *#About*
    - Group: 05
    - Topic: ML7 - A triple of LLMs: GPT-3, Megatron-Turing NLG, and Gemini
    - Description: Utilize large language models (LLMs) like GPT-3, Megatron-Turing NLG, and Gemini in building a robust question-answering system 
    to perform data chat, data analysis and data visualization.
    
    ### *#Usage*
    - Build a question-answering system that can process natural language queries related to data, extract relevant information from datasets, and provide clear answers and insights to users.
    - Use the LLMs for text analysis tasks like sentiment analysis, anomaly detection, and identifying unusual patterns in financial news, social media mentions, and other textual data sources.
    - Combine the insights from the LLMs with visualizations to create interactive dashboards for data-driven decision-making.

    ### *#Check out for demos*
    - [Data analysis system with Gemini]
    - [Question-Answering system with GPT-3]
    - [Data Visualization with GPT-3]
    
    **👈 Select a demo from the sidebar**!
"""
)