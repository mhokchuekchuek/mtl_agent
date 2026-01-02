#!/bin/bash
# Run SQLite migrations
# Usage: ./scripts/run_migrations.sh

set -e

DB_PATH="${1:-data/erp_database.db}"
MIGRATIONS_DIR="data/migrations"
APPLIED_FILE="$MIGRATIONS_DIR/.applied_migrations"

# Create applied migrations tracking file if not exists
touch "$APPLIED_FILE"

echo "Running migrations on: $DB_PATH"

# Find and run all .sql files in order
for migration in "$MIGRATIONS_DIR"/*.sql; do
    if [ -f "$migration" ]; then
        migration_name=$(basename "$migration")

        # Check if already applied
        if grep -q "^$migration_name$" "$APPLIED_FILE" 2>/dev/null; then
            echo "  [SKIP] $migration_name (already applied)"
        else
            echo "  [RUN]  $migration_name"
            sqlite3 "$DB_PATH" < "$migration"
            echo "$migration_name" >> "$APPLIED_FILE"
            echo "  [DONE] $migration_name"
        fi
    fi
done

echo "Migrations completed!"
