#!/bin/bash

# Prompt for username and password
read -p "Enter username: " username
read -sp "Enter password: " password
echo

# API endpoint (replace with your actual API endpoint)
api_url="https://qam.qntmnet.com/api/login"

# Send credentials to API
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{"username":"'"$username"'", "password":"'"$password"'"}' $api_url)

# Extract token from the response (assuming the token is in JSON format)
token=$(echo $response | jq -r '.token')

# Check if the token was received
if [ "$token" != "null" ] && [ -n "$token" ]; then
  #echo "Authentication successful. Token: $token"
  echo "$response" 
  # If the token is valid, run the package or main functionality
  #echo "Running the package..."
  # Place your package execution commands here
  #sysinfo  # Replace with the actual command to run your package

else
  echo "Authentication failed. No valid token received."
  exit 1
fi
