import re

import sqlglot

from sqlglot import exp


def validate_sql(sql_query):

    """
    Validates SQL queries using SQLGlot.

    Allows:
        - SELECT statements
        - Read-only CTE queries

    Rejects:
        - INSERT
        - UPDATE
        - DELETE
        - DROP
        - ALTER
        - CREATE
        - TRUNCATE
        - Multiple SQL statements
        - Invalid SQL syntax
    """

    if not sql_query or not sql_query.strip():
        return {
            "valid": False,
            "message": "SQL query cannot be empty."
        }

    try:

        # Parse using PostgreSQL dialect
        parsed_queries = sqlglot.parse(
            sql_query,
            read="postgres"
        )

        # Reject multiple statements
        if len(parsed_queries) != 1:
            return {
                "valid": False,
                "message": "Multiple SQL statements are not allowed."
            }

        parsed_query = parsed_queries[0]

        if parsed_query is None:
            return {
                "valid": False,
                "message": "Unable to parse SQL query."
            }

        # Only SELECT statements are allowed.
        # A read-only WITH ... SELECT query is also accepted.
        if not isinstance(parsed_query, exp.Select):
            return {
                "valid": False,
                "message": (
                    "Only SELECT queries and read-only "
                    "CTE queries are permitted."
                )
            }

        # Reject data-modifying operations anywhere in the SQL AST
        # including inside CTEs and nested expressions.
        dangerous_operations = {
            "insert",
            "update",
            "delete",
            "create",
            "drop",
            "alter",
            "merge",
            "command",
            "truncate"
        }

        for node in parsed_query.walk():

            if node.key.lower() in dangerous_operations:

                return {
                    "valid": False,
                    "message": (
                        "Data-modifying operations are not permitted."
                    )
                }

        # Reject SELECT INTO
        if parsed_query.args.get("into") is not None:
            return {
                "valid": False,
                "message": "SELECT INTO statements are not allowed."
            }

        # Reject row-locking queries
        if re.search(
            r"\bFOR\s+(UPDATE|SHARE|NO\s+KEY\s+UPDATE|KEY\s+SHARE)\b",
            sql_query,
            re.IGNORECASE
        ):
            return {
                "valid": False,
                "message": "Row-locking queries are not allowed."
            }

        # Check for dangerous sequence-modification functions
        if re.search(
            r"\b(nextval|setval)\s*\(",
            sql_query,
            re.IGNORECASE
        ):
            return {
                "valid": False,
                "message": "Sequence-modifying functions are not allowed."
            }

        return {
            "valid": True,
            "message": "SQL validation successful.",
            "sql": parsed_query.sql(dialect="postgres")
        }

    except sqlglot.errors.ParseError as error:

        return {
            "valid": False,
            "message": f"SQL syntax validation failed: {error}"
        }

    except Exception as error:

        return {
            "valid": False,
            "message": f"SQL validation error: {error}"
        }
