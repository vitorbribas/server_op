#!/bin/bash
set -e

host="$1"
shift

until PGPASSWORD=postgres psql -h "db" -U "postgres" -c '\q'; do
 echo 'Waiting for PostgreSQL...'
 sleep 1
done
echo "PostgreSQL is up and running!"

# If the database exists, migrate. Otherwise setup (create and migrate)
python3 manage.py makemigrations app && python3 manage.py migrate

echo "PostgreSQL database has been created & migrated!"

# Remove a potentially pre-existing server.pid for Django.
rm -f tmp/pids/server.pid

python3 manage.py runserver 0.0.0.0:8000