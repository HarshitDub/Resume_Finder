# main.py

import streamlit as st
from dotenv import load_dotenv
import ui

# Load .env variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Profile Scraper",
    layout="centered"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Title
st.title("🔎 AI Profile Scraper & Emailer")

# Conditional rendering
if not st.session_state["logged_in"]:
    ui.show_login()
else:
    ui.show_scraper_ui()
