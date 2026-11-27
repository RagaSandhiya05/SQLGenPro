from sqlalchemy import inspect
from app.database.connection import get_database_engine


def get_database_schema():
    """
    Extract database tables, columns, primary keys,
    foreign keys, unique constraints and data types.
    """

    engine = get_database_engine()
    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names(schema="public")

    for table_name in tables:

        columns = inspector.get_columns(
            table_name,
            schema="public"
        )

        primary_key_info = inspector.get_pk_constraint(
            table_name,
            schema="public"
        )

        foreign_keys = inspector.get_foreign_keys(
            table_name,
            schema="public"
        )

        unique_constraints = inspector.get_unique_constraints(
            table_name,
            schema="public"
        )

        primary_keys = (
            primary_key_info.get("constrained_columns") or []
        )

        unique_columns = set()

        for constraint in unique_constraints:
            unique_columns.update(
                constraint.get("column_names") or []
            )

        foreign_key_columns = set()

        for foreign_key in foreign_keys:
            foreign_key_columns.update(
                foreign_key.get("constrained_columns") or []
            )

        column_details = []

        for column in columns:

            column_name = column["name"]

            column_details.append({
                "name": column_name,
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "primary_key": column_name in primary_keys,
                "unique": column_name in unique_columns,
                "foreign_key": column_name in foreign_key_columns,
                "default": (
                    str(column["default"])
                    if column["default"] is not None
                    else None
                )
            })

        schema[table_name] = {
            "columns": column_details,
            "primary_keys": primary_keys,
            "foreign_keys": foreign_keys,
            "unique_constraints": unique_constraints
        }

    return schema


def get_database_relationships(schema=None):
    """
    Extract foreign-key relationships between tables.
    Accepts an existing schema to avoid repeated extraction.
    """

    if schema is None:
        schema = get_database_schema()

    relationships = []

    for table_name, details in schema.items():

        for foreign_key in details["foreign_keys"]:

            relationships.append({
                "source_table": table_name,
                "source_columns": (
                    foreign_key["constrained_columns"] or []
                ),
                "target_table": foreign_key["referred_table"],
                "target_columns": (
                    foreign_key["referred_columns"] or []
                )
            })

    return relationships


def get_schema_summary():
    """
    Return high-level database statistics.
    """

    schema = get_database_schema()

    relationships = get_database_relationships(schema)

    total_tables = len(schema)

    total_columns = sum(
        len(details["columns"])
        for details in schema.values()
    )

    total_primary_keys = sum(
        len(details["primary_keys"])
        for details in schema.values()
    )

    return {
        "total_tables": total_tables,
        "total_columns": total_columns,
        "total_primary_keys": total_primary_keys,
        "total_relationships": len(relationships)
    }


def format_schema_for_llm():
    """
    Convert database metadata into readable
    context for the Groq LLM.
    """

    schema = get_database_schema()

    relationships = get_database_relationships(schema)

    schema_context = []

    for table_name, details in schema.items():

        schema_context.append(
            f"TABLE: {table_name}"
        )

        for column in details["columns"]:

            description = (
                f"  - {column['name']} "
                f"({column['type']})"
            )

            if column["primary_key"]:
                description += " PRIMARY KEY"

            if column["foreign_key"]:
                description += " FOREIGN KEY"

            if column["unique"]:
                description += " UNIQUE"

            if not column["nullable"]:
                description += " NOT NULL"

            schema_context.append(description)

        schema_context.append("")

    if relationships:

        schema_context.append("DATABASE RELATIONSHIPS:")

        for relation in relationships:

            source = ", ".join(relation["source_columns"])
            target = ", ".join(relation["target_columns"])

            schema_context.append(
                f"  {relation['source_table']} ({source}) "
                f"REFERENCES "
                f"{relation['target_table']} ({target})"
            )

    return "\n".join(schema_context)
