import requests
import os
import sys
from dotenv import load_dotenv  # ✅ NEW

# Ensure UTF-8 encoding for I/O
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ✅ Load environment variables from .env file
load_dotenv()

# Load Pastebin API key from environment variables
PASTEBIN_API_KEY = os.getenv("PASTEBIN_API")

# Debugging: Check if the API key is loaded
if PASTEBIN_API_KEY is None:
    print("❌ ERROR: PASTEBIN_API environment variable not found!")
    exit(1)
else:
    print(f"✅ Loaded API Key: {PASTEBIN_API_KEY[:5]}********")

# Convert Google Sheet link to CSV format
def get_csv_url(sheet_url):
    if "edit" in sheet_url:
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    return sheet_url

# Fetch data from Google Sheets
def fetch_google_sheet_data(sheet_url):
    csv_url = get_csv_url(sheet_url)
    response = requests.get(csv_url)
    
    if response.status_code == 200:
        return response.text
    else:
        print("Error fetching Google Sheet data:", response.status_code)
        return None

# Post data to Pastebin
def post_to_pastebin(data):
    url = "https://pastebin.com/api/api_post.php"
    payload = {
        "api_dev_key": PASTEBIN_API_KEY,
        "api_option": "paste",
        "api_paste_code": data,
        "api_paste_private": "1",
        "api_paste_format": "text",
        "api_paste_name": "Google Sheet Data",
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200 and "pastebin.com" in response.text:
        return response.text
    else:
        print("Error posting to Pastebin:", response.text)
        return None

# Main function
if __name__ == "__main__":
    google_sheet_link = input("Enter your Google Sheet link: ")
    
    data = fetch_google_sheet_data(google_sheet_link)
    if data:
        paste_url = post_to_pastebin(data)
        if paste_url:
            print("✅ Data posted successfully:", paste_url)
        else:
            print("❌ Failed to post data.")