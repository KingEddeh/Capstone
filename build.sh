#!/usr/bin/env bash
set -o errexit

# Install dependencies with increased timeout
pip install -r requirements.txt 

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate