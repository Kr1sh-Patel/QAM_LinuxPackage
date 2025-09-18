import subprocess
import json

def get_usb_info():
    info = {
        "isEnabled": "0"
    }
    
    try:
        # Check if any USB devices are listed
        devices_output = subprocess.check_output(["lsusb"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).decode().strip()
        if devices_output:
            info["isEnabled"] = "1"
        else:
            info["isEnabled"] = "0"
    except subprocess.CalledProcessError:
        info["isEnabled"] = "0"
    except Exception as e:
        info["isEnabled"] = "0"
    
    return [info]

usb_info = get_usb_info()

print(json.dumps(usb_info, indent=4))
