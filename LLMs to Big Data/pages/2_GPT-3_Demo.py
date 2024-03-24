from dotenv import load_dotenv
import os
import streamlit as st
from pandasai import SmartDataframe
import pandas as pd
from pandasai.llm.openai import OpenAI
from pandasai.responses.response_parser import ResponseParser
from PIL import Image
from pandasai import Agent

load_dotenv()
llm = OpenAI(api_token = os.environ['OPEN_API_KEY'])

st.set_page_config(page_title="Data Chat", page_icon=":chart_with_upwards_trend:")
st.markdown(
    """
    <div style="text-align: center;">
        <h1>Data Chat</h1>
        <h3>Talk to your data</h3>
        <p>The Data Chat site helps analyze and interrogate your dataset based on natural language prompts</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload a csv file", type=['csv'])

class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)
        
    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return
    
    def format_plot(self, result):
        img = Image.open(result["value"])
        st.image(img)
        
        # st.image(result["value"])
        return 
        
    def format_other(self, result):
        st.write(result["value"])
        return

if uploaded_file != None:
    df = pd.read_csv(uploaded_file)
    with st.expander("Dataframe Preview"):
        st.write(df.head(5))
    
    prompt = st.text_area("Enter your promt: ")
    
    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                data = SmartDataframe(df, config={"llm": llm, "response_parser": StreamlitResponse})
                st.write(data.chat(prompt))
        else:
            st.warning("Please enter a prompt")
    