#!/usr/bin/env python3
import os
import json
import subprocess

def get_installed_gui_applications():
    apps = []

    # Command to list installed applications using 'dpkg-query'
    command = "dpkg-query -Wf '${Installed-Size}\t${Version}\t${Package}\n'"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    if result.returncode != 0:
        print("Error running dpkg-query:", result.stderr)
        return apps

    for line in result.stdout.splitlines():
        size, version, package = line.split("\t")
        # Filter only GUI applications
        # You can improve this filtering by checking for specific desktop files or categories
        if any(keyword in package for keyword in ['gui', 'desktop', 'x11', 'gnome', 'kde']):
            apps.append({
                "size": size,
                "version": version,
                "displayName": package
            })

    return apps

# Get the list of installed GUI applications
gui_apps = get_installed_gui_applications()

# Output the result in JSON format
json_output = json.dumps(gui_apps, indent=4)
print(json_output)
