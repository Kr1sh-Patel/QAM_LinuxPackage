#!/usr/bin/env python3
import json
import netifaces
import psutil

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
        "operationalStatus": 2
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
                info['speed'] = f"{speed / 1000000:.2f} Mb/s"  # Format speed in Mbps

        # Get MTU
        try:
            # MTU retrieval using netifaces
            mtu = netifaces.ifaddresses(iface).get(netifaces.AF_LINK, [{}])[0].get('mtu', 'Unknown')
            info["mtu"] = mtu
        except KeyError:
            info["mtu"] = "Unknown"

        # Set description and interfaceType to 'Unknown' as placeholders
        # You might need additional libraries or methods to accurately get these values
        info["description"] = "Unknown"  # Example placeholder
        info["interfaceType"] = "Unknown"  # Example placeholder
        info["isReceiveOnly"] = False  # Example placeholder

        # Determine operational status (up or down)
        if 'addr' in netifaces.ifaddresses(iface).get(netifaces.AF_INET, [{}])[0]:
            info["operationalStatus"] = 1
        else:
            info["operationalStatus"] = 2

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
