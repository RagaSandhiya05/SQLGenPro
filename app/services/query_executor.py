import time
import pandas as pd

from sqlalchemy import text

from app.database.connection import get_database_engine
from app.services.sql_validator import validate_sql


MAX_ROWS = 500
QUERY_TIMEOUT_MS = 15000


def execute_sql(sql_query):
    """
    Validates and executes read-only SQL queries
    against PostgreSQL.
    """

    # First validate the query
    validation = validate_sql(sql_query)

    if not validation["valid"]:
        raise ValueError(validation["message"])

    engine = get_database_engine()

    start_time = time.perf_counter()

    try:

        with engine.connect() as connection:

            with connection.begin():

                # Enforce a read-only PostgreSQL transaction
                connection.execute(
                    text("SET TRANSACTION READ ONLY")
                )

                # Set execution timeout
                connection.execute(
                    text(
                        f"SET LOCAL statement_timeout = "
                        f"'{QUERY_TIMEOUT_MS}ms'"
                    )
                )

                # Execute validated query
                result = connection.execute(
                    text(validation["sql"])
                )

                # Retrieve only MAX_ROWS + 1 rows
                columns = list(result.keys())

                rows = result.fetchmany(MAX_ROWS + 1)

                truncated = len(rows) > MAX_ROWS

                rows = rows[:MAX_ROWS]

                dataframe = pd.DataFrame(
                    [tuple(row) for row in rows],
                    columns=columns
                )

        execution_time = (
            time.perf_counter() - start_time
        )

        return {
            "success": True,
            "data": dataframe,
            "row_count": len(dataframe),
            "truncated": truncated,
            "execution_time": round(execution_time, 4),
            "message": "Query executed successfully."
        }

    except Exception as error:

        raise RuntimeError(
            f"PostgreSQL execution failed: {error}"
        ) from error
