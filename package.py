#!/usr/bin/env python3
import platform
import subprocess
import textwrap
import re 
import os

########## system-info code starts here #########

def get_system_info():
    info = {}

    # OS Information
    info['OS Name'] = platform.system()
    info['OS Version'] = platform.version()
    info['OS Release'] = platform.release()
    info['OS Distribution'] = platform.platform()
    
    # Machine Information
    info['Architecture'] = platform.architecture()[0]
    info['Machine'] = platform.machine()
    info['Processor'] = platform.processor()
    
    # CPU Information
    try:
        cpu_info = subprocess.check_output("lscpu", shell=True, universal_newlines=True)
        info['CPU Info'] = format_text(cpu_info, width=100)
    except Exception as e:
        info['CPU Info'] = f"Error retrieving CPU info: {str(e)}"
    
    # Memory Information
    try:
        mem_info = subprocess.check_output("free -h", shell=True, universal_newlines=True)
        info['Memory Info'] = format_text(mem_info, width=100)
    except Exception as e:
        info['Memory Info'] = f"Error retrieving memory info: {str(e)}"
    
    # Disk Information
    try:
        disk_info = subprocess.check_output("df -h", shell=True, universal_newlines=True)
        info['Disk Info'] = format_text(disk_info, width=100)
    except Exception as e:
        info['Disk Info'] = f"Error retrieving disk info: {str(e)}"
    
    # System Uptime
    try:
        uptime_info = subprocess.check_output("uptime -p", shell=True, universal_newlines=True)
        info['Uptime'] = format_text(uptime_info.strip(), width=100)
    except Exception as e:
        info['Uptime'] = f"Error retrieving uptime info: {str(e)}"
    
    # Network Information
    try:
        network_info = subprocess.check_output("ip a", shell=True, universal_newlines=True)
        info['Network Info'] = format_text(network_info, width=100)
    except Exception as e:
        info['Network Info'] = f"Error retrieving network info: {str(e)}"
    
    # Manufacturer and Device Information
    try:
        manufacturer_info = subprocess.check_output("dmidecode -t system", shell=True, universal_newlines=True)
        info['Manufacturer Info'] = format_text(manufacturer_info, width=100)
    except Exception as e:
        info['Manufacturer Info'] = f"Error retrieving manufacturer info: {str(e)}"
    
    return info

def format_text(text, width=80):
    # Wrap text to ensure readability
    lines = text.splitlines()
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    return "\n".join(wrapped_lines)

def print_section(title, content):
    # Print the title and content with formatting
    print(f"{title.upper()}:")
    print("=" * len(title))
    print(content)
    print()

def print_system_info(info):
    # Print formatted system information
    for key, value in info.items():
        print_section(key, value)

################ system-info code ends here ######################

################ browser code starts here ########################

def get_executable_paths():

    title = "BROWSER STATUS"
    print(f"{title}:")
    print("=" * len(title))

    # List of common installation directories
    common_directories = [
        '/usr/bin',
        '/usr/local/bin',
        '/opt/google/chrome',  # Add other common directories if needed
        '/opt/vivaldi',        # Add common directories here
        '/opt/brave',          # Add common directories here
        '/opt/librewolf',      # Add common directories here
        '/snap/bin'            # Add Snap bin directory
    ]
    
    # Combine PATH directories with common installation directories
    paths = os.environ["PATH"].split(os.pathsep) + common_directories
    executables = []  # Use a set to avoid duplicate entries
    
    for path in paths:
        if os.path.isdir(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.access(file_path, os.X_OK) and not os.path.isdir(file_path):
                    executables.append(file)  # Store the full path of the executable

    return set(executables)


def get_browser_version(command):
    try:
        output = subprocess.check_output(f"{command} --version", shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
        version = re.search(r"(\d+\.\d+\.\d+\.\d+|\d+\.\d+\.\d+|\d+\.\d+)", output)
        if version:
            return version.group(0)
    except subprocess.CalledProcessError:
        return None

def identify_browsers():
    executables = get_executable_paths()
    possible_browsers = ["chrome", "google-chrome", "chromium", "firefox", "safari", "opera", "brave", "vivaldi", "edge", "msedge", "tor", "librewolf"]

    browsers_found = {}
    for browser in possible_browsers:
        if browser in executables:
            version = get_browser_version(browser)
            if version:
                browsers_found[browser] = version

    # Additional checks for common installation paths
    common_paths = {
        "google-chrome": "/opt/google/chrome/google-chrome",
    }
    for browser, path in common_paths.items():
        if os.path.isfile(path) and os.access(path, os.X_OK):
            version = get_browser_version(path)
            if version:
                browsers_found[browser] = version

    return browsers_found

################ browser code ends here ##########################

################ firewall code starts here #######################

def get_firewall_status():
    status = {}

    # Check UFW status
    try:
        ufw_status = subprocess.check_output("sudo ufw status verbose", shell=True, text=True)
        status['UFW Status'] = ufw_status
    except subprocess.CalledProcessError:
        status['UFW Status'] = "UFW not installed or not active."

    return status

def print_firewall_status(status):
    for key, value in status.items():
        print(f"{key}:\n{'=' * len(key)}\n{value}\n")


################# firewall code ends here ########################


if __name__ == "__main__":

########## system-info statements starts here ####################
    system_info = get_system_info()
    print_system_info(system_info)
################ system-info statements ends here ################


################# browser statements starts here #################
    browsers = identify_browsers()
    if not browsers:
        print("No browsers found.")
    else:
        for browser, version in browsers.items():
            print(f"{browser.capitalize()}: {version}")
    print("\n")
################## browser statements ends here ##################


################# firewall statements starts here ################
    firewall_status = get_firewall_status()
    print_firewall_status(firewall_status)
################### firewall statements ends here ################
