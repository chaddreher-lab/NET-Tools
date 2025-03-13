import sys
import os
import subprocess
import psutil
import platform
import socket
import requests

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 6):
        print("Warning: Python version is below 3.6, which may cause compatibility issues.")
    print()

def check_installed_packages():
    print("Checking installed packages...")
    try:
        installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode("utf-8")
        print("Installed Packages:")
        print(installed_packages)
    except subprocess.CalledProcessError as e:
        print(f"Error checking installed packages: {e}")
    print()

def check_environment_variables():
    print("Checking environment variables...")
    env_vars = os.environ
    important_vars = ["PATH", "HOME", "USER", "PYTHONPATH"]
    for var in important_vars:
        value = env_vars.get(var, "Not Set")
        print(f"{var}: {value}")
    print()

def check_network_connectivity():
    print("Checking network connectivity...")
    try:
        # Check if we can connect to google.com
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("Network connectivity is working.")
        else:
            print(f"Unable to connect to the internet. HTTP Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Network check failed: {e}")
    print()

def check_disk_space():
    print("Checking disk space...")
    disk = psutil.disk_usage('/')
    print(f"Total disk space: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used disk space: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Free disk space: {disk.free / (1024 ** 3):.2f} GB")
    print(f"Disk usage percentage: {disk.percent}%")
    print()

def check_system_info():
    print("Checking system information...")
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    print()

def check_memory_usage():
    print("Checking memory usage...")
    memory = psutil.virtual_memory()
    print(f"Total memory: {memory.total / (1024 ** 3):.2f} GB")
    print(f"Used memory: {memory.used / (1024 ** 3):.2f} GB")
    print(f"Free memory: {memory.free / (1024 ** 3):.2f} GB")
    print(f"Memory usage percentage: {memory.percent}%")
    print()

def check_python_executable():
    print("Checking Python executable location...")
    print(f"Python executable: {sys.executable}")
    print()

def check_open_ports():
    print("Checking for open ports...")
    open_ports = []
    for port in range(1024, 65535):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            if result == 0:
                open_ports.append(port)
    if open_ports:
        print("Open ports:", open_ports)
    else:
        print("No open ports found.")
    print()

def environment_checks():
    check_python_version()
    check_installed_packages()
    check_environment_variables()
    check_network_connectivity()
    check_disk_space()
    check_system_info()
    check_memory_usage()
    check_python_executable()
    check_open_ports()

if __name__ == "__main__":
    environment_checks()