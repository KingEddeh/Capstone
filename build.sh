#!/usr/bin/env bash
set -o errexit

# Install dependencies with increased timeout
pip install -r requirements.txt 

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# # Create superuser automatically
# python manage.py shell -c "
# from django.contrib.auth.models import User;
# import os;
# username = 'admin';
# email = 'admin@dhvsu.edu.ph';
# password = 'admin';
# if not User.objects.filter(username=username).exists():
#     User.objects.create_superuser(username, email, password);
#     print('Superuser created successfully');
# else:
#     print('Superuser already exists');
# "