"""SQL database selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class SQLSelector(BaseToolSelector):
    """Selector for SQL database providers.

    Available providers:
        - sqlite: SQLite database

    Example:
        >>> from libs.database.sql.selector import SQLSelector
        >>> db = SQLSelector.create(
        ...     provider="sqlite",
        ...     db_path="data/erp_database.db"
        ... )
        >>> tables = db.get_tables()
        >>> results = db.query("SELECT * FROM Products LIMIT 5")
    """

    _PROVIDERS = {
        "sqlite": "libs.database.sql.sqlite.main.SQLiteClient",
    }
