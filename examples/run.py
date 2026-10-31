"""Minimal example: run the north-america-jobs-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "keywords": "engineer",
    "countries": ["US", "CA"],
    "maxItems": 50,
    "includeDescriptions": False,
}

run = client.actor("bibian/north-america-jobs-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    count += 1
    print(f"{item['title']} | {item.get('companyName')} | {item.get('country')} | {item.get('source')}")
print(f"{count} results")
