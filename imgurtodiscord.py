import requests

def post_to_discord_webhook(imgur_url, webhook_url):
    # Prepare the JSON payload for Discord
    data = {
        "content": "Here is an image from Imgur:",  # Optional message
        "embeds": [
            {
                "image": {
                    "url": imgur_url  # The Imgur image URL to embed in Discord
                }
            }
        ]
    }

    # Send a POST request to the Discord webhook
    response = requests.post(webhook_url, json=data)

    # Check if the request was successful
    if response.status_code == 204:
        print("Image successfully posted to Discord!")
    else:
        print(f"Failed to post image to Discord. Status code: {response.status_code}, Error: {response.text}")

# Usage example:
imgur_url = "https://i.imgur.com/yourimage.png"  # Replace with the Imgur link
webhook_url = "https://discord.com/api/webhooks/your_webhook_url"  # Replace with your Discord webhook URL

post_to_discord_webhook(imgur_url, webhook_url)