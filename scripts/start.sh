#!/bin/sh

set -e
DB_HOST='postgres-fastapi'
DB_PORT=5432

if [ -n "$DB_HOST" -a -n "$DB_PORT" ]
then
    while ! nc -vz "${DB_HOST}" "${DB_PORT}"; do
        echo "Waiting for database..."
        sleep 1;
    done
fi


alembic upgrade head && \
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
