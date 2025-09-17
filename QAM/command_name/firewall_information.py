import subprocess
import json

def get_ufw_status():
    try:
        result = subprocess.run(['sudo', 'ufw', 'status', 'verbose'], capture_output=True, text=True)
        output = result.stdout
        
        # Default values
        firewall_info = {
            "domainFirewall": "0",
            "publicFirewall": "0",
            "isAccessAllowed": "0",
            "privateFirewall": "0"
        }

        # Parsing `ufw` status output
        for line in output.splitlines():
            if 'Status:' in line:
                if 'active' in line:
                    firewall_info["isAccessAllowed"] = "1"
            if 'Default' in line:
                if 'allow' in line:
                    firewall_info["isAccessAllowed"] = "1"
            if 'To' in line:
                if 'Anywhere' in line:
                    if 'Public' in line:
                        firewall_info["publicFirewall"] = "1"
                    elif 'Private' in line:
                        firewall_info["privateFirewall"] = "1"
            if 'Anywhere' in line:
                if 'Domain' in line:
                    firewall_info["domainFirewall"] = "1"

        return json.dumps([firewall_info], indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

print(get_ufw_status())
