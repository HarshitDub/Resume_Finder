# scraper.py

from apify_client import ApifyClient
import pandas as pd
import time

# Set your Apify API token
APIFY_API_TOKEN = "your_apify_token_here"  # Replace or set via .env

def scrape_linkedin_profiles(query: str, max_results=20):
    """
    query: search string like 'data scientist in India at Google'
    max_results: number of profiles to scrape (up to actor's limit)
    """
    client = ApifyClient(APIFY_API_TOKEN)

    run_input = {
        "queries": [query],
        "resultsLimit": max_results,
        "maxConcurrency": 10,
        "language": "en",
        "location": "",
        "enhanceProfiles": True
    }

    print("🚀 Starting Apify LinkedIn Scraper...")
    run = client.actor("apify/linkedin-profile-scraper").call(run_input=run_input)

    items = client.dataset(run["defaultDatasetId"]).list_items().get("items", [])
    print(f"✅ {len(items)} profiles scraped.")

    # Extract useful fields
    data = []
    for item in items:
        data.append({
            "name": item.get("fullName"),
            "headline": item.get("headline"),
            "location": item.get("location"),
            "url": item.get("url"),
            "current_company": item.get("jobCompany"),
            "job_title": item.get("jobTitle"),
            "job_description": item.get("summary"),
            "connections": item.get("connectionsCount")
        })

    return pd.DataFrame(data)
