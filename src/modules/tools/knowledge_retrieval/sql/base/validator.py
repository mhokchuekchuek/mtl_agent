"""SQL security validation for dynamic queries."""

import re

from libs.logger.logger import get_logger

logger = get_logger(__name__)


class SQLValidator:
    """Validates SQL queries for security.

    Prevents execution of dangerous SQL statements like:
    - DROP, ALTER, CREATE, TRUNCATE (always forbidden)
    - DELETE, UPDATE, INSERT (forbidden unless allow_write=True)
    - Multiple statements (SQL injection via semicolon)
    - Comments that might hide malicious code
    """

    # Always forbidden - destructive DDL operations
    ALWAYS_FORBIDDEN = [
        r"\bDROP\b",
        r"\bALTER\b",
        r"\bCREATE\b",
        r"\bTRUNCATE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bEXEC\b",
        r"\bEXECUTE\b",
        r"\bATTACH\b",
        r"\bDETACH\b",
    ]

    # Write operations - allowed when allow_write=True
    WRITE_KEYWORDS = [
        r"\bDELETE\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bREPLACE\b",
    ]

    # Dangerous keywords that indicate write operations (for backward compat)
    FORBIDDEN_KEYWORDS = ALWAYS_FORBIDDEN + WRITE_KEYWORDS

    # Patterns for SQL injection attempts
    INJECTION_PATTERNS = [
        r";\s*\w",  # Multiple statements
        r"--",  # SQL comments
        r"/\*",  # Block comments
    ]

    def __init__(self, allow_union: bool = False, allow_write: bool = False):
        """Initialize validator.

        Args:
            allow_union: Whether to allow UNION SELECT (for complex queries).
            allow_write: Whether to allow write operations (INSERT, UPDATE, DELETE).
        """
        self.allow_union = allow_union
        self.allow_write = allow_write

        # Build forbidden patterns based on allow_write
        forbidden = self.ALWAYS_FORBIDDEN.copy()
        if not allow_write:
            forbidden.extend(self.WRITE_KEYWORDS)

        # Compile regex patterns for efficiency
        self._forbidden_pattern = re.compile("|".join(forbidden), re.IGNORECASE)

        injection_patterns = self.INJECTION_PATTERNS.copy()
        if not allow_union:
            injection_patterns.append(r"\bUNION\b.*\bSELECT\b")

        self._injection_pattern = re.compile(
            "|".join(injection_patterns), re.IGNORECASE
        )

    def is_safe(self, sql: str) -> bool:
        """Check if SQL query is safe to execute.

        Args:
            sql: SQL query string to validate.

        Returns:
            True if query is safe, False otherwise.
        """
        if not sql or not sql.strip():
            logger.warning("Empty SQL query")
            return False

        # Normalize whitespace
        normalized = " ".join(sql.split())

        # Check for forbidden keywords
        if self._forbidden_pattern.search(normalized):
            match = self._forbidden_pattern.search(normalized)
            logger.warning(
                f"Forbidden keyword detected: {match.group() if match else 'unknown'}"
            )
            return False

        # Check for injection patterns
        if self._injection_pattern.search(normalized):
            match = self._injection_pattern.search(normalized)
            logger.warning(
                f"Injection pattern detected: {match.group() if match else 'unknown'}"
            )
            return False

        # Check valid starting keyword
        valid_starts = ["SELECT"]
        if self.allow_write:
            valid_starts.extend(["INSERT", "UPDATE", "DELETE"])

        starts_valid = any(normalized.upper().startswith(kw) for kw in valid_starts)
        if not starts_valid:
            logger.warning(f"Query must start with one of: {valid_starts}")
            return False

        logger.debug("SQL validation passed")
        return True

    def sanitize(self, sql: str) -> str | None:
        """Attempt to sanitize SQL query.

        This is a best-effort sanitization. If the query cannot be
        safely sanitized, returns None.

        Args:
            sql: SQL query to sanitize.

        Returns:
            Sanitized SQL or None if not possible.
        """
        if not sql:
            return None

        # Remove comments
        sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
        sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)

        # Take only the first statement
        if ";" in sql:
            sql = sql.split(";")[0]

        sql = sql.strip()

        # Validate the sanitized query
        if self.is_safe(sql):
            return sql

        return None
