import streamlit as st
import google.generativeai as genai
import pandas as pd 

GOOGLE_API_KEY = "AIzaSyBqOvuNlu67wagkcCCuAvR_ytgIfQY36u4"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="SQL Query Generator ", page_icon=":robot:")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1>SQL Query Generator</h1>
                <h3>I can generate SQL queries for you</h3>
                <h4>With Explaination as well!!!</h4>
                <p>This tool is a simple tool that allows you to generate SQL queries based on your prompts.</p>
            </div>
        """,
        unsafe_allow_html=True
    )

    text_input = st.text_area("Enter your prompt here:")
    uploaded_file = st.file_uploader("Choose a CSV file (optional):")
    data = None

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data preview:")
        st.dataframe(data.head())

    submit=st.button("Generate SQL Query")
    if submit:
        with st.spinner("Generating SQL Query..."):
            template = """
                Create a SQL query snippet using below text:
                ```
                    {text_input}
                ```
                I just want a SQL Query
            """
            formatted_template = template.format(text_input=text_input)

            st.write(formatted_template)
            response = model.generate_content(formatted_template)
            sql_query = response.text
            st.write(sql_query)
            if data is not None and st.checkbox("Execute query on uploaded data?"):
                try:
                    # Execute the query on the dataframe 'data'
                    result = data.query(sql_query)
                    st.write("Query Results:")
                    st.dataframe(result)
                except Exception as e:
                    st.error(f"Error executing query: {e}")

main()