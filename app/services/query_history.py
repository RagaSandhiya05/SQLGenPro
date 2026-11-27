from sqlalchemy import text

from app.database.connection import get_database_engine


def initialize_history_table():
    """
    Creates the query history table if it does not exist.
    """

    engine = get_database_engine()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS sqlgenpro_query_history (

        id BIGSERIAL PRIMARY KEY,

        user_question TEXT NOT NULL,

        generated_sql TEXT NOT NULL,

        execution_time DOUBLE PRECISION NOT NULL,

        rows_returned INTEGER NOT NULL,

        executed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.begin() as connection:

        connection.execute(
            text(create_table_query)
        )


def save_query_history(
    user_question,
    generated_sql,
    execution_time,
    rows_returned
):
    """
    Saves a successfully executed query.
    """

    engine = get_database_engine()

    insert_query = text("""
        INSERT INTO sqlgenpro_query_history (
            user_question,
            generated_sql,
            execution_time,
            rows_returned
        )
        VALUES (
            :user_question,
            :generated_sql,
            :execution_time,
            :rows_returned
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            insert_query,
            {
                "user_question": user_question,
                "generated_sql": generated_sql,
                "execution_time": execution_time,
                "rows_returned": rows_returned
            }
        )


def get_query_history(search_term=None):
    """
    Retrieves saved query history.
    Supports searching by question or SQL.
    """

    engine = get_database_engine()

    if search_term:

        query = text("""
            SELECT
                id,
                user_question,
                generated_sql,
                execution_time,
                rows_returned,
                executed_at
            FROM sqlgenpro_query_history
            WHERE
                user_question ILIKE :search
                OR generated_sql ILIKE :search
            ORDER BY executed_at DESC, id DESC
        """)

        parameters = {
            "search": f"%{search_term}%"
        }

    else:

        query = text("""
            SELECT
                id,
                user_question,
                generated_sql,
                execution_time,
                rows_returned,
                executed_at
            FROM sqlgenpro_query_history
            ORDER BY executed_at DESC, id DESC
        """)

        parameters = {}

    with engine.connect() as connection:

        result = connection.execute(
            query,
            parameters
        )

        return [
            dict(row)
            for row in result.mappings().all()
        ]


def delete_query_history(history_id):
    """
    Deletes one query history record.
    """

    engine = get_database_engine()

    delete_query = text("""
        DELETE FROM sqlgenpro_query_history
        WHERE id = :history_id
    """)

    with engine.begin() as connection:

        result = connection.execute(
            delete_query,
            {"history_id": history_id}
        )

        return result.rowcount > 0
