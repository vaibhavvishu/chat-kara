#!/bin/bash
set -e
echo "Starting build process..."
python3.12 -m pip install -r requirements.txt --break-system-packages
echo "Running collectstatic..."
python3.12 manage.py collectstatic --noinput --clear
