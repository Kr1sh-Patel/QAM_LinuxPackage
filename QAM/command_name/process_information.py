#!/usr/bin/env python3
import psutil
import socket
import json

def get_processes_info():
    processes = []
    csname = socket.gethostname()

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_affinity', 'ppid', 'nice']):
        try:
            pinfo = proc.info
            process_info = {
                "Name": pinfo['name'],
                "CSName": csname,
                "Caption": pinfo['name'],
                "Priority": str(pinfo['nice']),
                "ProcessId": str(pinfo['pid']),
                "VirtualSize": str(pinfo['memory_info'].vms),
                "WorkingSetSize": str(pinfo['memory_info'].rss),
                "ParentProcessId": str(pinfo['ppid'])
            }
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return processes

if __name__ == "__main__":
    processes_info = get_processes_info()
    print(json.dumps(processes_info, indent=4))
