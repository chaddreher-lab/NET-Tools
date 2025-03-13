
import requests
from unifi_protect import ProtectApiClient
import time
import os

# UniFi Protect Credentials from Environment Variables
UNIFI_HOST = os.getenv("UNIFI_HOST")
UNIFI_USERNAME = os.getenv("UNIFI_USERNAME")
UNIFI_PASSWORD = os.getenv("UNIFI_PASSWORD")

# Discord Webhook
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("✅ Notification sent to Discord")
    else:
        print(f"❌ Failed to send message: {response.text}")

def monitor_unifi_cameras():
    client = ProtectApiClient(UNIFI_HOST, UNIFI_USERNAME, UNIFI_PASSWORD)
    print("📡 Connected to UniFi Protect")
    
    last_motion = {}
    
    while True:
        cameras = client.get_camera_list()
        for camera in cameras:
            motion_detected = camera.last_motion
            if motion_detected and camera.id not in last_motion:
                last_motion[camera.id] = motion_detected
                message = f"🚨 Motion detected on **{camera.name}** at `{motion_detected}`"
                send_to_discord(message)
            elif motion_detected and motion_detected != last_motion[camera.id]:
                last_motion[camera.id] = motion_detected
                message = f"📸 New motion detected on **{camera.name}** at `{motion_detected}`"
                send_to_discord(message)
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_unifi_cameras()