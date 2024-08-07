import subprocess
import json

def get_encryption_info():
    encryption_info = []

    try:
        # Get list of all block devices
        block_devices = subprocess.check_output(["lsblk", "-o", "NAME,TYPE,MOUNTPOINT", "-J"], text=True)
        block_devices_json = json.loads(block_devices)

        # Extract devices
        devices = block_devices_json.get("blockdevices", [])

        for device in devices:
            # Check if device is a disk or partition
            if device["type"] == "disk" or device["type"] == "part":
                device_name = device["name"]

                # Check if the device is encrypted
                try:
                    # Run cryptsetup to check for encryption
                    cryptsetup_output = subprocess.check_output(["cryptsetup", "status", device_name], text=True)
                    
                    # Parse cryptsetup output for encryption status
                    encryption_method = "Unknown"
                    protection_status = "0"  # Assuming not encrypted if status is unknown

                    if "device" in cryptsetup_output:
                        protection_status = "1"  # Device is encrypted

                        # Extract encryption method
                        if "LUKS1" in cryptsetup_output:
                            encryption_method = "1"  # Example encryption method code for LUKS1
                        elif "LUKS2" in cryptsetup_output:
                            encryption_method = "2"  # Example encryption method code for LUKS2

                    encryption_info.append({
                        "driveLetter": f"/dev/{device_name}",  # Using /dev/ path instead of drive letter
                        "encryptionMethod": encryption_method,
                        "protectionStatus": protection_status
                    })

                except subprocess.CalledProcessError:
                    # Handle cases where cryptsetup does not recognize the device
                    encryption_info.append({
                        "driveLetter": f"/dev/{device_name}",
                        "encryptionMethod": "Unknown",
                        "protectionStatus": "0"
                    })

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving encryption information: {e}")

    return encryption_info

def main():
    encryption_info = get_encryption_info()
    print(json.dumps(encryption_info, indent=4))

if __name__ == "__main__":
    main()
