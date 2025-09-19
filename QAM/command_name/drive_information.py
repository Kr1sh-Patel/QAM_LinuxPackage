#!/usr/bin/env python3
import json
import subprocess

def convert_to_bytes(size_str):
    """Convert human-readable size string to bytes."""
    size_str = size_str.strip().upper()
    units = {'B': 1, 'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}
    for unit in units:
        if size_str.endswith(unit):
            return int(float(size_str[:-len(unit)]) * units[unit])
    return int(size_str)

def get_disk_partitions():
    # Run 'df -h' to get the filesystem details
    df_output = subprocess.check_output(['df', '-h']).decode('utf-8').strip().split('\n')[1:]
    
    partitions = []
    
    for line in df_output:
        parts = line.split()
        if len(parts) >= 6:
            filesystem, size, used, available, percent, mountpoint = parts
            drive_id = mountpoint
            drive_name = drive_id
            drive_type = "3"  # Fixed hard disk (generic assumption)
            free_space = convert_to_bytes(available)  # Convert to bytes
            media_type = "Fixed hard disk media"
            file_system = filesystem
            total_space = convert_to_bytes(size)  # Convert to bytes
            volume_name = mountpoint  # Assuming mountpoint as volume name
            media_loaded = "True"
            media_status = "OK"
            capabilities = "System.UInt16[]"  # Placeholder
            drive_compressed = "False"  # Placeholder

            partitions.append({
                "driveId": drive_id,
                "driveName": drive_name,
                "driveType": drive_type,
                "freeSpace": str(free_space),
                "mediaType": media_type,
                "fileSystem": file_system,
                "totalSpace": str(total_space),
                "volumeName": volume_name,
                "mediaLoaded": media_loaded,
                "mediaStatus": media_status,
                "capabilities": capabilities,
                "driveCompressed": drive_compressed
            })

    return partitions

def main():
    partitions = get_disk_partitions()
    print(json.dumps(partitions, indent=4))

if __name__ == "__main__":
    main()
