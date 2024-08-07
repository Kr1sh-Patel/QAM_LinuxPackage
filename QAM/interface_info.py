import json
import netifaces
import psutil
import subprocess

def is_valid_interface_type(iface):
    """
    Determine if the interface is valid for processing.
    This can be customized to filter out virtual interfaces or loopback interfaces.
    """
    return iface not in ['lo']  # Example filter; customize as needed

def get_interface_info(iface):
    """
    Retrieve detailed information about a network interface.
    """
    info = {
        "name": iface,
        "mac_address": "Unknown",
        "ip_addresses": [],
        "speed": "Unknown",
        "isShared": "0",
        "description": "Unknown",
        "interfaceType": "Unknown",
        "isReceiveOnly": False,
        "operationalStatus": 2,  # Default to down
        "mtu": "Unknown"
    }

    try:
        if not is_valid_interface_type(iface):
            return None  # Skip processing invalid interfaces

        # Get the MAC address
        if netifaces.AF_LINK in netifaces.ifaddresses(iface):
            info["mac_address"] = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']

        # Get the IP addresses
        info["ip_addresses"] = [addr['addr'] for family in netifaces.ifaddresses(iface).keys()
                                for addr in netifaces.ifaddresses(iface)[family]
                                if family in (netifaces.AF_INET, netifaces.AF_INET6)]

        # Get speed using psutil
        nic_stats = psutil.net_if_stats()
        if iface in nic_stats:
            speed = nic_stats[iface].speed
            if speed > 0:
                info['speed'] = f"{speed} bps"  # Speed in bits per second

        # Get MTU using system command
        try:
            result = subprocess.run(['ip', 'link', 'show', iface], capture_output=True, text=True)
            mtu_line = [line for line in result.stdout.splitlines() if 'mtu' in line]
            if mtu_line:
                info["mtu"] = mtu_line[0].split('mtu')[1].split()[0]
        except Exception as e:
            info["mtu"] = "Error fetching MTU"

        # Try to get description and interfaceType
        try:
            result = subprocess.run(['ethtool', iface], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if 'Driver:' in line:
                    info["description"] = line.split(':')[1].strip()
        except Exception as e:
            info["description"] = "Error fetching description"

        # Update operational status based on IP address presence
        if info["ip_addresses"]:
            info["operationalStatus"] = 1  # Up

    except Exception as e:
        print(f"Error processing interface {iface}: {e}")
        return None

    return info

def main():
    """
    Main function to collect and display network interface information.
    """
    interfaces = netifaces.interfaces()
    interface_data = []

    for iface in interfaces:
        interface_info = get_interface_info(iface)
        if interface_info:
            interface_data.append(interface_info)

    print(json.dumps(interface_data, indent=4))

if __name__ == "__main__":
    main()
