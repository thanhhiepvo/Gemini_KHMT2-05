import streamlit as st
import google.generativeai as genai
import pandas as pd

GOOGLE_API_KEY = "AIzaSyBsrdz-9jVMyzlu-E_Tc4d_t51fwC34tXw"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="Data Analysis", page_icon=":chart_with_upwards_trend:")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Data Analysis</h1>
            <h3>Understand your data</h3>
            <p>The Data Analysis site helps generate descriptions or insights about your dataset based on natural language prompts</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload a csv file", type=['csv'])

    if uploaded_file != None:
        data = pd.read_csv(uploaded_file)
        with st.expander("Dataframe Preview"):
            st.write(data.head(5))
            
        text_input = st.text_area("Enter a prompt about the data (e.g., 'summarize key statistics', 'find trends'):")
        if st.button("Generate"):
            if text_input:
                with st.spinner("Generating response..."):
                    template = f"""
                        Analyze the data in the uploaded CSV file based on the prompt: {text_input}
                        The dataset: {data}
                    """
                    formatted_template = template.format(text_input=text_input)
                    #st.write(formatted_template)
            else:
                st.warning("Please enter a prompt")

            response = model.generate_content(formatted_template)
            analysis = response.text
            st.write("Analysis:")
            st.write(analysis)

if __name__ == "__main__":
    main()