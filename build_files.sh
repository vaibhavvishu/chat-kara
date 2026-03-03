#!/bin/bash
set -e
echo "Starting build process..."
python3.9 -m pip install -r requirements.txt --break-system-packages
echo "Running collectstatic..."
python3.9 manage.py collectstatic --noinput --clear
