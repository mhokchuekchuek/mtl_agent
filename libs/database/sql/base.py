"""Base abstraction for SQL databases."""

from abc import ABC, abstractmethod
from typing import Any


class BaseSQLDatabase(ABC):
    """Abstract base class for SQL databases.

    All SQL database implementations must inherit from this class and implement
    all abstract methods. This enables swapping between different SQL databases
    (SQLite, PostgreSQL, MySQL, etc.) without changing application code.
    """

    @abstractmethod
    def execute(self, query: str, params: tuple = ()) -> int:
        """Execute a write query (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query string with ? placeholders
            params: Tuple of parameter values

        Returns:
            Number of rows affected

        Raises:
            Exception: If execution fails
        """
        pass

    @abstractmethod
    def query(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Execute a read query (SELECT).

        Args:
            query: SQL query string with ? placeholders
            params: Tuple of parameter values

        Returns:
            List of rows as dictionaries

        Raises:
            Exception: If query fails
        """
        pass

    @abstractmethod
    def get_tables(self) -> list[str]:
        """Get list of all table names in the database.

        Returns:
            List of table names

        Raises:
            Exception: If query fails
        """
        pass

    @abstractmethod
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
            Exception: If query fails
        """
        pass

    @abstractmethod
    def get_db_type(self) -> str:
        """Get the database type identifier.

        Returns:
            Database type string (e.g., "sqlite", "postgresql", "mysql")
        """
        pass
