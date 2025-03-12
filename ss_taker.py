import pyautogui

def take_screenshot():
    """Take a screenshot and save it."""
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot saved as screenshot.png")
