import streamlit as st
import requests

# Display title
st.title('Sankey Graphic')

# Raw URL to the HTML file on GitHub
html_url = "https://raw.githubusercontent.com/jtferri/public-repository/refs/heads/main/sankey.html"

# Fetch the HTML content
response = requests.get(html_url)

if response.status_code == 200:
    plot_html = response.text
    st.components.v1.html(plot_html, height=600)
else:
    st.error("Failed to load the HTML file from GitHub.")
