from app.services.sql_validator import validate_sql


test_cases = [

    (
        "Simple SELECT",
        "SELECT * FROM users;",
        True
    ),

    (
        "Aggregate SELECT",
        "SELECT AVG(rating) FROM reviews;",
        True
    ),

    (
        "JOIN query",
        """
        SELECT r.restaurant_name, AVG(rv.rating)
        FROM restaurants r
        JOIN reviews rv
        ON r.restaurant_id = rv.restaurant_id
        GROUP BY r.restaurant_name;
        """,
        True
    ),

    (
        "Read-only CTE",
        """
        WITH restaurant_stats AS (
            SELECT restaurant_id, AVG(rating) AS avg_rating
            FROM reviews
            GROUP BY restaurant_id
        )
        SELECT * FROM restaurant_stats;
        """,
        True
    ),

    (
        "DELETE query",
        "DELETE FROM users;",
        False
    ),

    (
        "DROP query",
        "DROP TABLE users;",
        False
    ),

    (
        "UPDATE query",
        "UPDATE users SET city = 'Chennai';",
        False
    ),

    (
        "INSERT query",
        "INSERT INTO users VALUES (10, 'Test');",
        False
    ),

    (
        "Multiple statements",
        "SELECT * FROM users; DELETE FROM users;",
        False
    ),

    (
        "SELECT INTO",
        "SELECT * INTO backup_users FROM users;",
        False
    ),

    (
        "Row locking",
        "SELECT * FROM users FOR UPDATE;",
        False
    ),

    (
        "Sequence modification",
        "SELECT nextval('user_id_seq');",
        False
    )
]


print("\n" + "=" * 65)
print("SQLGenPro - SQL Validation Test Suite")
print("=" * 65)

passed = 0

for name, query, expected in test_cases:

    result = validate_sql(query)

    actual = result["valid"]

    if actual == expected:

        print(f"[PASS] {name}")
        passed += 1

    else:

        print(f"[FAIL] {name}")
        print(f"       Expected: {expected}")
        print(f"       Actual: {actual}")
        print(f"       Message: {result['message']}")


print("\n" + "=" * 65)
print(f"Test Results: {passed}/{len(test_cases)} passed")
print("=" * 65)
