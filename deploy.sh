#!/bin/bash
# Run this script on your OCI compute instance after SSH-ing in

sudo yum install -y python3 python3-pip git
cd /home/opc
git clone <YOUR_REPO_URL> app || true
cd app
pip3 install -r requirements.txt
# Start the app (use nohup to keep running after logout)
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
echo "App running on port 8000"
