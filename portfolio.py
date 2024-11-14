# portfolio.py

import os
import pandas as pd
import streamlit as st

# Define the Portfolio class here
class Portfolio:
    def __init__(self):
        self.data = None

    def load_portfolio(self, file_path):
        # Check if the portfolio file exists
        if not os.path.exists(file_path):
            print(f"Portfolio file '{file_path}' not found. Using default portfolio.")
            default_data = {
                'skill': ['python', 'data-science', 'java'],
                'link': ['https://example.com/python', 'https://example.com/data-science', 'https://example.com/java']
            }
            self.data = pd.DataFrame(default_data)
        else:
            self.data = pd.read_csv(file_path)
        print("Portfolio loaded successfully.")

    def query_links(self, skills):
        # Query the links based on skills
        if self.data is not None:
            matching_links = []
            for skill in skills:
                links = self.data[self.data['skill'] == skill]['link'].tolist()
                matching_links.extend(links)
            return matching_links
        else:
            print("Portfolio data is not loaded.")
            return []

# You don't need to import Portfolio in this file
