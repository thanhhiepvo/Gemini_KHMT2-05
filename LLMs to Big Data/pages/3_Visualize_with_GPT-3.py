from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import openai
import re

Model = "gpt-3.5-turbo"
load_dotenv()

st.set_option('deprecation.showPyplotGlobalUse', False)
openai.api_key = os.getenv('OPEN_API_KEY')

st.set_page_config(page_title="Data Visualization", page_icon=":chart_with_upwards_trend:")
st.markdown(
    """
    <div style="text-align: center;">
        <h1>Data Visualization</h1>
        <h3>Understand your data</h3>
        <p>The Data Visualization site helps plot your dataset based on natural language prompts</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload a csv file", type=['csv'])

def handle_openai_query(df, column_names, query):
    if query and query.strip() != "":
            # Define the prompt content
            prompt_content = f"""
            The dataset is ALREADY loaded into a DataFrame named 'df'. DO NOT load the data again.
            
            The DataFrame has the following columns: {column_names}
            
            Before plotting, ensure the data is ready:
            1. Check if columns that are supposed to be numeric are recognized as such. If not, attempt to convert them.
            2. Handle NaN values by filling with mean or median.
            
            Use package Pandas and Matplotlib ONLY.
            Provide SINGLE CODE BLOCK with a solution using Pandas and Matplotlib plots in a single figure to address the following query:
            
            {query}

            - USE SINGLE CODE BLOCK with a solution. 
            - Do NOT EXPLAIN the code 
            - DO NOT COMMENT the code. 
            - ALWAYS WRAP UP THE CODE IN A SINGLE CODE BLOCK.
            - The code block must start and end with ```
            
            - Example code format ```code```
        
            - Colors to use for background and axes of the figure : #F0F0F6
            - Try to use the following color palette for coloring the plots : #8f63ee #ced5ce #a27bf6 #3d3b41
            
            """

            # Define the messages for the OpenAI model
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful Data Visualization assistant who gives a single block without explaining or commenting the code to plot. IF ANYTHING NOT ABOUT THE DATA, JUST politely respond that you don't know.",
                },
                {"role": "user", "content": prompt_content},
            ]

            # Call OpenAI and display the response
            with st.status("📟 *Expand for code details*..."):
                with st.chat_message("assistant", avatar="📊"):
                    botmsg = st.empty()
                    response = []
                    for chunk in openai.ChatCompletion.create(
                        model=Model, messages=messages, stream=True
                    ):
                        text = chunk.choices[0].get("delta", {}).get("content")
                        if text:
                            response.append(text)
                            result = "".join(response).strip()
                            botmsg.write(result)
            execute_openai_code(result, df, query)
            
def extract_code_from_markdown(md_text):
    """
    Extract Python code from markdown text.

    Parameters:
    - md_text: Markdown text containing the code

    Returns:
    - The extracted Python code
    """
    # Extract code between the delimiters
    code_blocks = re.findall(r"```(python)?(.*?)```", md_text, re.DOTALL)

    # Strip leading and trailing whitespace and join the code blocks
    code = "\n".join([block[1].strip() for block in code_blocks])

    return code

def execute_openai_code(response_text: str, df: pd.DataFrame, query):
    """
    Execute the code provided by OpenAI in the app.

    Parameters:
    - response_text: The response text from OpenAI
    - df: DataFrame containing the data
    - query: The user's query
    """

    # Extract code from the response text
    code = extract_code_from_markdown(response_text)

    # If there's code in the response, try to execute it
    if code:
        try:
            exec(code)
            st.pyplot()
        except Exception as e:
            error_message = str(e)
            st.error(
                f"📟 Apologies, failed to execute the code due to the error: {error_message}"
            )
            st.warning(
                """
                📟 Check the error message and the code executed above to investigate further.

                Pro tips:
                - Tweak your prompts to overcome the error 
                - Use the words 'Plot'/ 'Subplot'
                - Use simpler, concise words
                - Remember, I'm specialized in displaying charts not in conveying information about the dataset
            """
            )
    else:
        st.write(response_text)

if uploaded_file != None:
    df = pd.read_csv(uploaded_file)
    with st.expander("Dataframe Preview"):
        st.write(df.head(5))
        
    query = st.text_area("Enter your promt: ")
    if st.button("Generate"):
        if query:
            with st.spinner("Generating response..."):
                column_names = ", ".join(df.columns)
                handle_openai_query(df, column_names, query)
        else:
            st.warning("Please enter a prompt")