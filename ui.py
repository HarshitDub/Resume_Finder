# ui.py

import streamlit as st
import pandas as pd
from scraper import scrape_linkedin_profiles
from emailer import send_email_gmail, send_email_ses
from utils import get_download_link_excel, get_download_link_csv, export_to_excel, export_to_csv

def show_login():
    st.header("🔐 Login or Signup")
    auth_mode = st.radio("Choose mode", ["Login", "Signup"], horizontal=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.button("Submit")

    if submit:
        init_auth_storage()
        if auth_mode == "Signup":
            if signup(email, password):
                st.success("✅ Signup successful! Please log in.")
            else:
                st.error("❌ Email already registered.")
        elif auth_mode == "Login":
            if login(email, password):
                st.success("✅ Login successful")
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
            else:
                st.error("❌ Invalid credentials")

def show_scraper_ui():
    st.header("🌐 Profile Scraper")

    with st.form("scrape_form"):
        role = st.text_input("Role (e.g. Data Scientist)")
        experience = st.text_input("Experience filter (e.g. 3+ years)")
        company = st.text_input("Company filter (optional)")
        max_results = st.slider("Number of profiles", min_value=5, max_value=50, value=10)
        source = f"{role} with {experience} experience"
        if company:
            source += f" at {company}"
        submit = st.form_submit_button("🔍 Fetch Profiles")

    if submit:
        with st.spinner("Fetching profiles..."):
            df = scrape_linkedin_profiles(source, max_results)
            st.session_state["scraped_df"] = df
            st.success(f"✅ Scraped {len(df)} profiles")

    if "scraped_df" in st.session_state:
        df = st.session_state["scraped_df"]
        st.subheader("📊 Preview")
        st.dataframe(df)

        st.markdown("---")
        st.subheader("📥 Export Options")
        st.markdown(get_download_link_excel(df), unsafe_allow_html=True)
        st.markdown(get_download_link_csv(df), unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📧 Send to Email")

        user_email = st.text_input("Recipient Email", value=st.session_state.get("user_email", ""))
        method = st.radio("Choose method", ["Gmail SMTP", "AWS SES"])

        if st.button("Send Email"):
            filepath = export_to_excel(df)
            body = "Attached are the scraped LinkedIn profiles as requested."

            if method == "Gmail SMTP":
                success = send_email_gmail(user_email, "Scraped Profiles Report", body, filepath)
            else:
                success = send_email_ses(user_email, "Scraped Profiles Report", body, filepath)

            if success:
                st.success("✅ Email sent successfully.")
            else:
                st.error("❌ Failed to send email.")
