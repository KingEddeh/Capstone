#!/usr/bin/env bash
set -o errexit

# Upgrade pip first
python -m pip install --upgrade pip

# Install build dependencies for pandas
pip install wheel setuptools

# Install dependencies with increased timeout
pip install -r requirements.txt --timeout=300

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate