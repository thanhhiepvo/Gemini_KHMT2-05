import streamlit as st
import google.generativeai as genai
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBqOvuNlu67wagkcCCuAvR_ytgIfQY36u4"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="Data Analyzer", page_icon=":chart_with_upwards_trend:")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Data Analyzer</h1>
            <h3>Understand your data</h3>
            <p>Our machine helps generate descriptions or insights based on your prompts with your dataset.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    text_input = st.text_area("Enter a prompt about the data (e.g., 'summarize key statistics', 'find trends'):")
    uploaded_file = st.file_uploader("Choose a CSV file:")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data preview:")
        st.dataframe(data.head())

        if text_input:
            template = f"""
                Analyze the data in the uploaded CSV file based on the prompt: {text_input}
                The dataset: {data}
            """
            formatted_template = template.format(text_input=text_input)
            #st.write(formatted_template)

            response = model.generate_content(formatted_template)
            analysis = response.text
            st.write("Analysis:")
            st.write(analysis)

if __name__ == "__main__":
    main()