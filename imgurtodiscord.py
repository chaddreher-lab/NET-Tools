import requests

def post_images_to_discord_webhook(imgur_urls, webhook_url):
    embeds = []
    for url in imgur_urls:
        if url:  # Skip empty inputs
            embeds.append({
                "image": {
                    "url": url
                }
            })

    if not embeds:
        print("No valid Imgur URLs provided.")
        return

    data = {
        "content": "Here are the images from Imgur:",
        "embeds": embeds
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Images successfully posted to Discord!")
    else:
        print(f"Failed to post images. Status code: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    webhook_url = input("Enter the Discord webhook URL: ").strip()

    print("Enter Imgur image URLs (one per line). Press Enter on a blank line to finish.")
    imgur_urls = []
    while True:
        url = input("Imgur URL: ").strip()
        if not url:
            break
        imgur_urls.append(url)

    post_images_to_discord_webhook(imgur_urls, webhook_url)