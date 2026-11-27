from sqlalchemy import text
from app.database.connection import get_database_engine


def initialize_saved_queries_table():
    engine = get_database_engine()

    query = """
    CREATE TABLE IF NOT EXISTS sqlgenpro_saved_queries (
        id BIGSERIAL PRIMARY KEY,
        title VARCHAR(150) NOT NULL,
        description TEXT,
        sql_query TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """

    with engine.begin() as connection:
        connection.execute(text(query))


def save_query(title, description, sql_query):
    engine = get_database_engine()

    query = text("""
        INSERT INTO sqlgenpro_saved_queries
        (title, description, sql_query)
        VALUES (:title, :description, :sql_query)
    """)

    with engine.begin() as connection:
        connection.execute(query, {
            "title": title,
            "description": description,
            "sql_query": sql_query
        })


def get_saved_queries(search_term=None):
    engine = get_database_engine()

    query = """
        SELECT id, title, description, sql_query,
               created_at, updated_at
        FROM sqlgenpro_saved_queries
    """

    parameters = {}

    if search_term:
        query += """
            WHERE title ILIKE :search
               OR description ILIKE :search
               OR sql_query ILIKE :search
        """
        parameters["search"] = f"%{search_term}%"

    query += " ORDER BY updated_at DESC, id DESC"

    with engine.connect() as connection:
        result = connection.execute(text(query), parameters)
        return [dict(row) for row in result.mappings().all()]


def update_saved_query(query_id, title, description, sql_query):
    engine = get_database_engine()

    query = text("""
        UPDATE sqlgenpro_saved_queries
        SET title = :title,
            description = :description,
            sql_query = :sql_query,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :query_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {
            "query_id": query_id,
            "title": title,
            "description": description,
            "sql_query": sql_query
        })

        return result.rowcount > 0


def delete_saved_query(query_id):
    engine = get_database_engine()

    query = text("""
        DELETE FROM sqlgenpro_saved_queries
        WHERE id = :query_id
    """)

    with engine.begin() as connection:
        result = connection.execute(query, {"query_id": query_id})
        return result.rowcount > 0
