# main.py

import os
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

# Import the Portfolio class from portfolio.py
from portfolio import Portfolio
from chains import Chain
from utils import clean_text

# Set the USER_AGENT environment variable to avoid the warning
os.environ[
    'USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # User inputs URL
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load the webpage content
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Check if portfolio file exists before trying to load it
            portfolio_path = "app/resource/my_portfolio.csv"
            print("Checking portfolio file at:", os.path.abspath(portfolio_path))  # Debug print
            if not os.path.exists(portfolio_path):
                st.error(f"Portfolio file '{portfolio_path}' not found. Using default portfolio data.")
                portfolio.load_portfolio(None)  # Load default portfolio data
            else:
                portfolio.load_portfolio(portfolio_path)

            # Extract job details from the content
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.warning("No jobs found in the provided URL.")

            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)  # Get links based on skills
                email = llm.write_mail(job, links)  # Generate cold email
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()  # Initialize Portfolio class
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
