from app.llm.groq_client import generate_completion

from app.database.schema_intelligence import (
    format_schema_for_llm
)


SYSTEM_PROMPT = """
You are SQLGenPro, an expert PostgreSQL query generation assistant.

Your responsibility is to convert natural-language questions
into accurate PostgreSQL SQL queries.

STRICT RULES:

1. Generate SQL compatible with PostgreSQL.

2. Use only tables and columns present in the
   supplied database schema.

3. Understand foreign-key relationships before
   generating JOIN operations.

4. Use appropriate aggregate functions such as
   COUNT, SUM, AVG, MIN and MAX.

5. Use GROUP BY and ORDER BY wherever necessary.

6. Use meaningful aliases for calculated columns.

7. Use LIMIT when the user requests a specific
   number of records.

8. Never invent table names or column names.

9. Do not generate INSERT, UPDATE, DELETE, DROP,
   ALTER, CREATE or TRUNCATE statements.

10. Only generate read-only SELECT queries.
    CTEs using WITH are allowed when they lead
    to a read-only SELECT query.

11. If the question cannot be answered using
    the supplied schema, explain the limitation
    instead of inventing SQL.

12. Do not execute SQL.

OUTPUT FORMAT:

Return only the SQL query.

Do not include Markdown code fences.
Do not include explanations before or after SQL.
"""


def clean_sql_response(response):
    """
    Removes Markdown code fences if returned
    by the language model.
    """

    response = response.strip()

    if response.startswith("```sql"):
        response = response[6:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


def generate_sql(user_question):
    """
    Converts a natural-language question
    into PostgreSQL SQL using Groq.
    """

    if not user_question or not user_question.strip():
        raise ValueError(
            "Please enter a valid question."
        )

    database_schema = format_schema_for_llm()

    user_prompt = f"""
DATABASE SCHEMA:

{database_schema}

USER QUESTION:

{user_question}

Generate the appropriate PostgreSQL query
using only the supplied database schema.
"""

    response = generate_completion(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt
    )

    return clean_sql_response(response)
