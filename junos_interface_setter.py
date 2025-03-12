def build_interface_config(interface, description, vlan_id):
    config_commands = [
        f"set interfaces {interface} description \"{description}\"",
        f"set interfaces {interface} unit 0 family ethernet-switching vlan members {vlan_id}",
        f"set interfaces {interface} unit 0 family ethernet-switching storm-control default"
    ]
    return "\n".join(config_commands)

if __name__ == "__main__":
    interface = input("Enter interface (e.g., ge-0/0/1): ")
    description = input("Enter interface description: ")
    vlan_id = input("Enter VLAN ID: ")
    
    config = build_interface_config(interface, description, vlan_id)
    print("Generated Configuration:")
    print(config)