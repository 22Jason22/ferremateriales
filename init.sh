#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h db -p 5432 -U ${DB_USER}; do
  sleep 1
done

echo "Database is ready!"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "from users.models import CustomUser; CustomUser.objects.filter(username='admin').exists() or CustomUser.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "Initialization complete!"
