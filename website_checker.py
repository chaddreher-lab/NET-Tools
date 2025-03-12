import requests

def check_website(url):
    """Check if a website is up."""
    try:
        response = requests.get(url)
        print(f"{url} is {'UP' if response.status_code == 200 else 'DOWN'}")
    except requests.RequestException:
        print(f"{url} is DOWN")