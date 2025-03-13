import requests
import json
import time

# UniFi Protect API settings
UNIFI_HOST = "https://your-unifi-host"
UNIFI_USERNAME = "your-username"
UNIFI_PASSWORD = "your-password"
UNIFI_SITE_ID = "default"  # Change if necessary

# Discord webhook settings
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-url"

# Function to get UniFi Protect access token
def get_unifi_token():
    url = f"{UNIFI_HOST}/api/auth/login"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"username": UNIFI_USERNAME, "password": UNIFI_PASSWORD})
    response = requests.post(url, headers=headers, data=data, verify=False)
    if response.status_code == 200:
        return response.cookies
    else:
        print("Failed to authenticate with UniFi Protect.")
        return None

# Function to get motion detections
def get_camera_detections(cookies):
    url = f"{UNIFI_HOST}/proxy/protect/api/events"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch camera detections.")
        return []

# Function to send notifications to Discord
def send_to_discord(message):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# Main loop to poll for detections
def main():
    session_cookies = get_unifi_token()
    if not session_cookies:
        return

    last_event_time = None
    while True:
        detections = get_camera_detections(session_cookies)
        if detections:
            for event in detections:
                event_time = event.get("start")
                camera_name = event.get("camera")
                event_type = event.get("type")
                
                if last_event_time is None or event_time > last_event_time:
                    message = f"🚨 Motion detected on {camera_name}! Event Type: {event_type}"
                    send_to_discord(message)
                    last_event_time = event_time
        
        time.sleep(10)  # Adjust polling interval as needed

if __name__ == "__main__":
    main()
