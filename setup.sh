#!/bin/bash
echo "Downloading python's external modules..."
python3 -m pip install -r requirements.txt
echo "All python's external modules installed."
echo "Installing nodeJs..."
curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
sudo apt install nodejs -y
echo "Verifying the nodeJs version:"
node --version
sudo apt install build-essential
echo "Installing all the nodeJs modules for the website runs..."
cd notation-website
npm i
