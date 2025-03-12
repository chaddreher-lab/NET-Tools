import requests
import os

# Load Pastebin API key from environment variables
PASTEBIN_API_KEY = os.getenv("PASTEBIN_API")

# Convert Google Sheet link to CSV format
def get_csv_url(sheet_url):
    if "edit" in sheet_url:
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    return sheet_url  # Assume it's already a direct CSV link

# Fetch data from Google Sheets
def fetch_google_sheet_data(sheet_url):
    csv_url = get_csv_url(sheet_url)
    response = requests.get(csv_url)
    
    if response.status_code == 200:
        return response.text  # Raw CSV data
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
        "api_paste_private": "1",  # 0 = public, 1 = unlisted, 2 = private
        "api_paste_format": "text",  # FIX: Use "text" instead of "csv"
        "api_paste_name": "Google Sheet Data",
    }

    response = requests.post(url, data=payload)
    
    if response.status_code == 200 and "pastebin.com" in response.text:
        return response.text  # URL of the Pastebin post
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
            print("Data posted successfully:", paste_url)
        else:
            print("Failed to post data.")
