#!/bin/bash
# Run SQLite migrations
# Usage: ./scripts/run_migrations.sh [db_path]
#
# This script tracks migrations in a table inside the database itself,
# so if you replace the database file, migrations will be re-applied.

set -e

DB_PATH="${1:-data/erp_database.db}"
MIGRATIONS_DIR="data/migrations"

echo "Running migrations on: $DB_PATH"

# Create migrations tracking table if not exists
sqlite3 "$DB_PATH" "CREATE TABLE IF NOT EXISTS _migrations (
    name TEXT PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

# Find and run all .sql files in order
for migration in "$MIGRATIONS_DIR"/*.sql; do
    if [ -f "$migration" ]; then
        migration_name=$(basename "$migration")

        # Check if already applied (in database)
        applied=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM _migrations WHERE name = '$migration_name';")

        if [ "$applied" -gt 0 ]; then
            echo "  [SKIP] $migration_name (already applied)"
        else
            echo "  [RUN]  $migration_name"
            sqlite3 "$DB_PATH" < "$migration"
            sqlite3 "$DB_PATH" "INSERT INTO _migrations (name) VALUES ('$migration_name');"
            echo "  [DONE] $migration_name"
        fi
    fi
done

echo "Migrations completed!"
