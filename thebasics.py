import psutil
import socket
import requests
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def check_system_resources():
    """Check system CPU, Memory, and Disk Usage."""
    print("\n🖥️ **System Resource Usage:**")
    print(f"⚙️ CPU Usage: {psutil.cpu_percent(interval=1)}%")
    print(f"🧠 Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"💾 Disk Usage: {psutil.disk_usage('/').percent}%\n")

def check_internet():
    """Check Internet connectivity and DNS resolution with user-defined hostname."""
    hostname = input("🌍 Enter a hostname to check (default: google.com): ") or "www.google.com"
    
    print(f"\n🌍 **Network Check for {hostname}**:")
    try:
        requests.get(f"https://{hostname}", timeout=5)
        print("✅ Internet is working")
    except requests.ConnectionError:
        print("❌ No internet connection")

    try:
        resolved_ip = socket.gethostbyname(hostname)
        print(f"✅ DNS is resolving correctly to {resolved_ip}\n")
    except socket.gaierror:
        print("❌ DNS resolution failed\n")

def scan_ports():
    """Scan all ports (1-65535) and list open ones."""
    host = input("🔍 Enter IP to scan (default: 127.0.0.1): ") or "127.0.0.1"
    print(f"\n🔍 **Scanning all ports on {host} (1-65535):**")
    open_ports = []
    
    for port in range(1, 65536):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)  # Fast scanning
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
                print(f"🟢 Port {port} is open")
    
    if not open_ports:
        print("✅ No open ports found")
    else:
        print(f"\n✅ Open ports: {open_ports}\n")

def check_running_processes():
    """List running processes and their CPU usage."""
    print("\n📋 **Running Processes (Top CPU Users):**")
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
    for process in processes[:5]:  # Show top 5 CPU-consuming processes
        print(f"🔹 {process.info['name']} (PID: {process.info['pid']}) - {process.info['cpu_percent']}% CPU")
    print()

def check_system_logs():
    """Scan system logs for error messages."""
    log_file = "/var/log/syslog"  # Change for Windows: "C:\\Windows\\System32\\winevt\\Logs\\Application.evtx"
    
    print("\n📜 **System Log Errors:**")
    if os.path.exists(log_file):
        with open(log_file, 'r', errors='ignore') as file:
            errors = [line.strip() for line in file if "error" in line.lower()]
            if errors:
                for error in errors[:5]:  # Show first 5 errors
                    print(f"⚠️ {error}")
            else:
                print("✅ No recent errors found in logs.")
    else:
        print("❌ Log file not found.")
    print()

def main_menu():
    """Display an interactive menu for troubleshooting options."""
    while True:
        print("\n🛠️ **System Troubleshooting Menu** 🛠️")
        print("1️⃣ Check System Resource Usage")
        print("2️⃣ Check Internet & DNS")
        print("3️⃣ Scan All Ports")
        print("4️⃣ View Running Processes")
        print("5️⃣ Check System Logs")
        print("0️⃣ Exit")

        choice = input("👉 Select an option (0-5): ")

        if choice == "1":
            check_system_resources()
        elif choice == "2":
            check_internet()
        elif choice == "3":
            scan_ports()
        elif choice == "4":
            check_running_processes()
        elif choice == "5":
            check_system_logs()
        elif choice == "0":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 0-5.")

if __name__ == "__main__":
    main_menu()