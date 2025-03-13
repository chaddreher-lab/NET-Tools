import requests
import time
import os
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

# UniFi Protect Credentials from Environment Variables
UNIFI_HOST = os.getenv("UNIFI_HOST")
UNIFI_USERNAME = os.getenv("UNIFI_USERNAME")
UNIFI_PASSWORD = os.getenv("UNIFI_PASSWORD")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Validate Environment Variables
if not all([UNIFI_HOST, UNIFI_USERNAME, UNIFI_PASSWORD, DISCORD_WEBHOOK_URL]):
    print("❌ Missing required environment variables! Please set them in the .env file.")
    exit(1)

def send_to_discord(message, image_path=None):
    data = {"content": message}
    files = {"file": (os.path.basename(image_path), open(image_path, "rb"))} if image_path else None
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, data=data, files=files)
        response.raise_for_status()
        print("✅ Notification sent to Discord")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send message: {e}")
        if response is not None:
            print(f"Response: {response.text}")

def get_unifi_auth():
    url = f"{UNIFI_HOST}/api/auth/login"
    data = {"username": UNIFI_USERNAME, "password": UNIFI_PASSWORD}
    response = requests.post(url, json=data, verify=False)
    if response.status_code == 200:
        return response.cookies
    else:
        print("❌ Failed to authenticate with UniFi Protect")
        return None

def get_cameras(cookies):
    url = f"{UNIFI_HOST}/proxy/protect/api/cameras"
    response = requests.get(url, cookies=cookies, verify=False)
    if response.status_code == 200:
        cameras = response.json()
        if isinstance(cameras, list):  # Ensure it's a list
            return {"data": cameras}  # Wrap it in a dictionary to match expected format
        return cameras  # If it's already a dict, return as is
    else:
        print(f"❌ Failed to retrieve camera list: {response.status_code}")
        return {"data": []}  # Return a consistent structure

def get_camera_snapshot(cookies, camera_id):
    url = f"{UNIFI_HOST}/proxy/protect/api/cameras/{camera_id}/snapshot"
    response = requests.get(url, cookies=cookies, verify=False)
    if response.status_code == 200:
        snapshot_path = f"snapshot_{camera_id}.jpg"
        with open(snapshot_path, "wb") as file:
            file.write(response.content)
        return snapshot_path
    else:
        print(f"❌ Failed to retrieve snapshot for camera {camera_id}")
        return None

def monitor_unifi_cameras():
    cookies = get_unifi_auth()
    if not cookies:
        return
    print("📡 Connected to UniFi Protect")
    
    last_motion = {}
    
    while True:
        cameras = get_cameras(cookies)
        for camera in cameras.get("data", []):
            motion_detected = camera.get("lastMotion")
            camera_name = camera.get("name", "Unknown Camera")
            camera_id = camera.get("id")
            
            if motion_detected and camera_id not in last_motion:
                last_motion[camera_id] = motion_detected
                snapshot = get_camera_snapshot(cookies, camera_id)
                message = f"🚨 Motion detected on **{camera_name}** at <t:{int(motion_detected/1000)}:f>"
                send_to_discord(message, snapshot)
            elif motion_detected and motion_detected != last_motion[camera_id]:
                last_motion[camera_id] = motion_detected
                snapshot = get_camera_snapshot(cookies, camera_id)
                message = f"📸 New motion detected on **{camera_name}** at <t:{int(motion_detected/1000)}:f>"
                send_to_discord(message, snapshot)
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_unifi_cameras()
