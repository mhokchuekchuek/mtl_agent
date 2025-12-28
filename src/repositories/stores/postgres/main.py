"""Postgres store repository implementation."""

from typing import Any, Optional

import psycopg
from langgraph.store.base import BaseStore
from langgraph.store.postgres import PostgresStore

from src.repositories.stores.base import BaseStoreRepository


class PostgresStoreRepository(BaseStoreRepository):
    """Repository for Postgres-backed long-term memory.

    Uses LangGraph's PostgresStore for:
    - Conversation summaries
    - User preferences
    - Cross-thread memory sharing
    """

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        """Initialize PostgresStore with connection parameters.

        Args:
            host: Postgres host
            port: Postgres port
            database: Database name
            user: Database user
            password: Database password
        """
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self._conn = psycopg.connect(conn_string, autocommit=True)
        self._store = PostgresStore(conn=self._conn)
        self._store.setup()

    @property
    def store(self) -> BaseStore:
        """Get underlying store for workflow injection."""
        return self._store

    def put(
        self,
        namespace: tuple[str, ...],
        key: str,
        value: dict[str, Any],
    ) -> None:
        """Store a value."""
        self._store.put(namespace, key, value)

    def get(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> Optional[dict[str, Any]]:
        """Retrieve a value."""
        item = self._store.get(namespace, key)
        return item.value if item else None

    def search(
        self,
        namespace: tuple[str, ...],
        query: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search for values in namespace."""
        results = self._store.search(namespace, query=query, limit=limit)
        return [item.value for item in results]

    def delete(
        self,
        namespace: tuple[str, ...],
        key: str,
    ) -> None:
        """Delete a value."""
        self._store.delete(namespace, key)

    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            self._conn.close()
