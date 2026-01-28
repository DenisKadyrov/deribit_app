#!/usr/bin/env sh
set -e

echo "⏳ Waiting for database..."
until alembic upgrade head; do
  echo "DB not ready, retrying in 2s..."
  sleep 2
done

echo "✅ Migrations applied"

exec "$@"
