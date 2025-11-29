#!/bin/bash

# Exit on error
set -e

echo "Starting Django application..."

# Wait for database to be ready (if using PostgreSQL)
if [ "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    # Extract host and port from DATABASE_URL if needed
    # For now, just wait a bit
    sleep 2
fi

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist (optional)
# Uncomment these lines if you want to auto-create a superuser
# python manage.py shell << EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin')
# EOF

echo "Starting server..."

# Execute the main command (passed as arguments to this script)
exec "$@"
