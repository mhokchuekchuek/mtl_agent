"""SQLite database client.

Implements SQL database operations using SQLite.

Reference: https://docs.python.org/3/library/sqlite3.html
"""

import sqlite3
from typing import Any

from libs.database.sql.base import BaseSQLDatabase
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class SQLiteClient(BaseSQLDatabase):
    """SQLite database client.

    Provides SQL database operations for SQLite databases. SQLite is a
    lightweight, file-based database perfect for embedded applications.

    Features:
    - File-based storage (no server required)
    - Full SQL support
    - Thread-safe with check_same_thread=False
    - Dictionary-style row access

    Reference: https://docs.python.org/3/library/sqlite3.html
    """

    def __init__(self, db_path: str):
        """Initialize SQLite client.

        Args:
            db_path: Path to the SQLite database file

        Note:
            For the ERP database, use db_path="data/erp_database.db"
        """
        self.db_path = db_path
        self._connection: sqlite3.Connection | None = None

        logger.info(f"SQLite client initialized (db_path={db_path})")

    @property
    def connection(self) -> sqlite3.Connection:
        """Get or create database connection.

        Returns:
            SQLite connection with Row factory enabled
        """
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.db_path,
                check_same_thread=False,
            )
            self._connection.row_factory = sqlite3.Row
            logger.debug(f"Connected to SQLite database: {self.db_path}")
        return self._connection

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            logger.debug(f"Closed SQLite connection: {self.db_path}")

    def execute(self, query: str, params: tuple = ()) -> int:
        """Execute a write query (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query string with ? placeholders
            params: Tuple of parameter values

        Returns:
            Number of rows affected

        Raises:
            sqlite3.Error: If execution fails

        Example:
            >>> db.execute(
            ...     "UPDATE Products SET price = ? WHERE product_id = ?",
            ...     (99, 1)
            ... )
            1
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            rows_affected = cursor.rowcount

            logger.debug(
                f"Executed query: {query[:100]}... "
                f"(params={len(params)}, rows_affected={rows_affected})"
            )
            return rows_affected

        except sqlite3.Error as e:
            logger.error(f"Execute failed: {e}", exc_info=True)
            self.connection.rollback()
            raise

    def query(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute a read query (SELECT).

        Args:
            query: SQL query string with ? placeholders
            params: Tuple of parameter values

        Returns:
            List of rows as dictionaries

        Raises:
            sqlite3.Error: If query fails

        Example:
            >>> results = db.query(
            ...     "SELECT * FROM Products WHERE category = ?",
            ...     ("Electronics",)
            ... )
            >>> results[0]["product_name"]
            'Smartphone X'
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            results = [dict(row) for row in rows]

            logger.debug(
                f"Query executed: {query[:100]}... "
                f"(params={len(params)}, rows={len(results)})"
            )
            return results

        except sqlite3.Error as e:
            logger.error(f"Query failed: {e}", exc_info=True)
            raise

    def get_tables(self) -> list[str]:
        """Get list of all table names in the database.

        Returns:
            List of table names

        Raises:
            sqlite3.Error: If query fails

        Example:
            >>> db.get_tables()
            ['Products', 'Inventory', 'Orders', 'Customers', ...]
        """
        try:
            query = """
                SELECT name FROM sqlite_master
                WHERE type='table'
                ORDER BY name
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            tables = [row[0] for row in cursor.fetchall()]

            logger.debug(f"Found {len(tables)} tables")
            return tables

        except sqlite3.Error as e:
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
            sqlite3.Error: If query fails

        Example:
            >>> db.get_schema("Products")
            [
                {"name": "product_id", "type": "INTEGER", "nullable": False, "primary_key": True},
                {"name": "product_name", "type": "TEXT", "nullable": True, "primary_key": False},
                ...
            ]
        """
        try:
            query = f"PRAGMA table_info({table_name})"
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            schema = [
                {
                    "name": row[1],
                    "type": row[2],
                    "nullable": row[3] == 0,  # notnull=0 means nullable
                    "primary_key": row[5] == 1,
                }
                for row in rows
            ]

            logger.debug(f"Schema for '{table_name}': {len(schema)} columns")
            return schema

        except sqlite3.Error as e:
            logger.error(f"Get schema failed: {e}", exc_info=True)
            raise

    def get_full_schema(self) -> dict[str, list[dict[str, Any]]]:
        """Get schema for all tables in the database.

        This is a convenience method not in the base class.

        Returns:
            Dictionary mapping table names to their schemas

        Example:
            >>> schema = db.get_full_schema()
            >>> schema["Products"]
            [{"name": "product_id", ...}, ...]
        """
        tables = self.get_tables()
        return {table: self.get_schema(table) for table in tables}

    def get_db_type(self) -> str:
        """Get the database type identifier.

        Returns:
            "sqlite" as the database type
        """
        return "sqlite"

    def __enter__(self) -> "SQLiteClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - close connection."""
        self.close()
