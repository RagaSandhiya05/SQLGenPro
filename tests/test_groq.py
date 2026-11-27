from app.llm.groq_client import generate_completion
from app.llm.sql_generator import generate_sql


def test_groq_connection():

    print("\n" + "=" * 55)
    print("SQLGenPro - Groq API Connection Test")
    print("=" * 55)

    try:

        response = generate_completion(
            system_prompt="You are a helpful AI assistant.",
            user_prompt="Reply with exactly: SQLGenPro Groq integration successful!"
        )

        print("\nGroq Response:")
        print(response)

        return True

    except Exception as error:

        print("\nGroq Connection Failed:")
        print(error)

        return False


def test_sql_generation():

    print("\n" + "=" * 55)
    print("SQLGenPro - Text-to-SQL Generation Test")
    print("=" * 55)

    question = (
        "Show me the top 3 restaurants "
        "by average customer rating."
    )

    print("\nUser Question:")
    print(question)

    try:

        sql_query = generate_sql(question)

        print("\nGenerated PostgreSQL Query:")
        print("-" * 55)
        print(sql_query)
        print("-" * 55)

    except Exception as error:

        print("\nSQL Generation Failed:")
        print(error)


if __name__ == "__main__":

    connection_success = test_groq_connection()

    if connection_success:
        test_sql_generation()
