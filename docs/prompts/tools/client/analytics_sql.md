# Analytics SQL Prompt

Generate SQL for BI analytics queries.

## Location

`prompts/tools/client/analytics_sql.prompt`

## Prompt Name

`client_chatbot_analytics_sql`

## Purpose

Generate SQL queries to answer business intelligence analytics questions. Supports both SQLite and PostgreSQL with database-specific syntax.

## Input Variables

| Variable | Description |
|----------|-------------|
| `question` | User's analytics question |
| `schema` | Database schema definition |
| `db_type` | Database type (`sqlite` or `postgresql`) |

## Output Format

JSON object with SQL and explanation:

```json
{
  "sql": "SELECT ...",
  "explanation": "Brief explanation"
}
```

## Database-Specific Syntax

| Operation | SQLite | PostgreSQL |
|-----------|--------|------------|
| Monthly grouping | `strftime('%Y-%m', date)` | `DATE_TRUNC('month', date)` |
| Yearly grouping | `strftime('%Y', date)` | `DATE_TRUNC('year', date)` |
| Year extraction | `strftime('%Y', date)` | `EXTRACT(YEAR FROM date)` |

## Rules

1. READ-ONLY: Only SELECT queries allowed
2. Use exact table/column names from schema
3. Use appropriate JOINs for related data
4. Use aggregations (SUM, COUNT, AVG) for analytics
5. Use GROUP BY for breakdowns

## Example Queries

| Question | SQL Pattern |
|----------|-------------|
| Annual sales | `GROUP BY strftime('%Y', order_date)` |
| Sales by category | `JOIN Products ... GROUP BY category` |
| Top customers | `GROUP BY customer_id ORDER BY total DESC LIMIT 10` |
