import os
import platform
import subprocess

def ping_host(host):
    """Ping a host to check connectivity."""
    command = ["ping", "-c", "4", host] if platform.system() != "Windows" else ["ping", "-n", "4", host]
    subprocess.run(command)

def traceroute_host(host):
    """Perform a traceroute to a host."""
    command = ["traceroute", host] if platform.system() != "Windows" else ["tracert", host]
    subprocess.run(command)

def display_ip_config():
    """Show local network interface configuration."""
    command = ["ifconfig"] if platform.system() != "Windows" else ["ipconfig"]
    subprocess.run(command)

def test_dns_resolution(domain):
    """Check DNS resolution for a domain."""
    command = ["nslookup", domain] if platform.system() == "Windows" else ["dig", domain, "+short"]
    subprocess.run(command)

def check_port_connectivity(host, port):
    """Check if a specific port is open on a remote host."""
    if platform.system() == "Windows":
        command = ["powershell", "-Command", f"Test-NetConnection -ComputerName {host} -Port {port}"]
    else:
        command = ["nc", "-zv", host, str(port)]
    subprocess.run(command)

def test_internet_connectivity():
    """Check if the system can reach the internet."""
    command = ["ping", "-c", "4", "8.8.8.8"] if platform.system() != "Windows" else ["ping", "-n", "4", "8.8.8.8"]
    subprocess.run(command)

def speed_test():
    """Perform an internet speed test."""
    try:
        import speedtest
        st = speedtest.Speedtest()
        print("Downloading speed:", st.download() / 1_000_000, "Mbps")
        print("Uploading speed:", st.upload() / 1_000_000, "Mbps")
    except ImportError:
        print("Speedtest module not installed. Install it with 'pip install speedtest-cli'")

def display_arp_table():
    """Show ARP table to troubleshoot local network issues."""
    command = ["arp", "-a"]
    subprocess.run(command)

def ping_with_packet_size(host, size):
    """Ping a host with a specified packet size."""
    command = ["ping", "-c", "4", "-s", str(size), host] if platform.system() != "Windows" else ["ping", "-n", "4", "-l", str(size), host]
    subprocess.run(command)

if __name__ == "__main__":
    while True:
        print("\nNetwork Troubleshooting Options:")
        print("1. Ping a host")
        print("2. Traceroute to a host")
        print("3. Display IP configuration")
        print("4. Test DNS resolution")
        print("5. Check port connectivity")
        print("6. Test internet connectivity")
        print("7. Perform speed test")
        print("8. Display ARP table")
        print("9. Ping with custom packet size")
        print("10. Exit")
        
        choice = input("Select an option (1-10): ")
        
        if choice == "1":
            host = input("Enter host to ping: ")
            ping_host(host)
        elif choice == "2":
            host = input("Enter host for traceroute: ")
            traceroute_host(host)
        elif choice == "3":
            display_ip_config()
        elif choice == "4":
            domain = input("Enter domain to resolve: ")
            test_dns_resolution(domain)
        elif choice == "5":
            host = input("Enter host: ")
            port = input("Enter port: ")
            check_port_connectivity(host, port)
        elif choice == "6":
            test_internet_connectivity()
        elif choice == "7":
            speed_test()
        elif choice == "8":
            display_arp_table()
        elif choice == "9":
            host = input("Enter host to ping: ")
            size = input("Enter packet size: ")
            ping_with_packet_size(host, size)
        elif choice == "10":
            print("Exiting...")
            break
        else:
            print("Invalid option, please try again.")