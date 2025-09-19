#!/usr/bin/env python3
import os
import json
import pwd
import grp

def get_user_info():
    users_information = []
    try:
        # Iterate over all users in the system
        for user in pwd.getpwall():
            user_info = {}
            user_info["Name"] = user.pw_name

            # Determine the domain (usually the hostname in a non-domain setup)
            user_info["Domain"] = os.uname().nodename

            # Get account type, typically based on UID and GID
            user_info["AccountType"] = str(user.pw_uid)

            # Check if it's a local account
            user_info["LocalAccount"] = "True" if user.pw_uid < 1000 else "False"

            # Describe the account type
            user_info["AccountTypeDesc"] = "Normal account" if user.pw_uid >= 1000 else "System account"

            users_information.append(user_info)
    except Exception as e:
        print(f"Error fetching user information: {e}")

    return users_information

def main():
    users_info = get_user_info()
    print(json.dumps({"users_information": users_info}, indent=4))

if __name__ == "__main__":
    main()
