"""PostgreSQL database client.

Implements SQL database operations using PostgreSQL with psycopg.

Reference: https://www.psycopg.org/psycopg3/docs/
"""

from typing import Any

import psycopg
from psycopg.rows import dict_row

from libs.database.sql.base import BaseSQLDatabase
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class PostgreSQLClient(BaseSQLDatabase):
    """PostgreSQL database client.

    Provides SQL database operations for PostgreSQL databases.

    Features:
    - Connection pooling ready
    - Dictionary-style row access
    - Full SQL support

    Reference: https://www.psycopg.org/psycopg3/docs/
    """

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        """Initialize PostgreSQL client.

        Args:
            host: PostgreSQL host
            port: PostgreSQL port
            database: Database name
            user: Database user
            password: Database password
        """
        self.conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self._connection: psycopg.Connection | None = None

        logger.info(f"PostgreSQL client initialized (host={host}, database={database})")

    @property
    def connection(self) -> psycopg.Connection:
        """Get or create database connection.

        Returns:
            PostgreSQL connection with dict row factory
        """
        if self._connection is None or self._connection.closed:
            self._connection = psycopg.connect(
                self.conn_string,
                autocommit=True,
                row_factory=dict_row,
            )
            logger.debug("Connected to PostgreSQL database")
        return self._connection

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            self._connection = None
            logger.debug("Closed PostgreSQL connection")

    def execute(self, query: str, params: tuple = ()) -> int:
        """Execute a write query (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query string with %s placeholders
            params: Tuple of parameter values

        Returns:
            Number of rows affected

        Raises:
            psycopg.Error: If execution fails
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                rows_affected = cursor.rowcount

            logger.debug(
                f"Executed query: {query[:100]}... "
                f"(params={len(params)}, rows_affected={rows_affected})"
            )
            return rows_affected

        except psycopg.Error as e:
            logger.error(f"Execute failed: {e}", exc_info=True)
            raise

    def query(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute a read query (SELECT).

        Args:
            query: SQL query string with %s placeholders
            params: Tuple of parameter values

        Returns:
            List of rows as dictionaries

        Raises:
            psycopg.Error: If query fails
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()

            logger.debug(
                f"Query executed: {query[:100]}... "
                f"(params={len(params)}, rows={len(results)})"
            )
            return results

        except psycopg.Error as e:
            logger.error(f"Query failed: {e}", exc_info=True)
            raise

    def get_tables(self) -> list[str]:
        """Get list of all table names in the database.

        Returns:
            List of table names

        Raises:
            psycopg.Error: If query fails
        """
        try:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                tables = [row["table_name"] for row in cursor.fetchall()]

            logger.debug(f"Found {len(tables)} tables")
            return tables

        except psycopg.Error as e:
            logger.error(f"Get tables failed: {e}", exc_info=True)
            raise

    def get_schema(self, table_name: str) -> list[dict[str, Any]]:
        """Get schema information for a table.

        Args:
            table_name: Name of the table

        Returns:
            List of column info dictionaries containing:
            {
                "name": str,
                "type": str,
                "nullable": bool,
                "primary_key": bool
            }

        Raises:
            psycopg.Error: If query fails
        """
        try:
            # Get column info
            query = """
                SELECT
                    c.column_name,
                    c.data_type,
                    c.is_nullable,
                    CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as is_primary_key
                FROM information_schema.columns c
                LEFT JOIN (
                    SELECT ku.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage ku
                        ON tc.constraint_name = ku.constraint_name
                    WHERE tc.table_name = %s
                        AND tc.constraint_type = 'PRIMARY KEY'
                ) pk ON c.column_name = pk.column_name
                WHERE c.table_name = %s
                    AND c.table_schema = 'public'
                ORDER BY c.ordinal_position
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query, (table_name, table_name))
                rows = cursor.fetchall()

            schema = [
                {
                    "name": row["column_name"],
                    "type": row["data_type"].upper(),
                    "nullable": row["is_nullable"] == "YES",
                    "primary_key": row["is_primary_key"],
                }
                for row in rows
            ]

            logger.debug(f"Schema for '{table_name}': {len(schema)} columns")
            return schema

        except psycopg.Error as e:
            logger.error(f"Get schema failed: {e}", exc_info=True)
            raise

    def __enter__(self) -> "PostgreSQLClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - close connection."""
        self.close()
