import streamlit as st

from app.services.query_history import (
    get_query_history,
    delete_query_history
)


def render_query_history():

    st.title("🕘 Query History")

    st.caption(
        "Explore, search and reuse previously executed SQL queries."
    )

    st.divider()

    # Search
    search_term = st.text_input(
        "🔍 Search Query History",
        placeholder="Search questions or SQL statements..."
    )

    try:

        history = get_query_history(
            search_term.strip() or None
        )

    except Exception as error:

        st.error(
            f"Unable to retrieve query history: {error}"
        )

        return

    if not history:

        st.info(
            "No query history found. Execute a SQL query "
            "from the AI SQL Assistant to get started."
        )

        return

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Queries",
        len(history)
    )

    col2.metric(
        "Total Rows Returned",
        sum(item["rows_returned"] for item in history)
    )

    average_time = (
        sum(item["execution_time"] for item in history)
        / len(history)
    )

    col3.metric(
        "Average Execution Time",
        f"{average_time:.4f}s"
    )

    st.divider()

    st.subheader("Previously Executed Queries")

    for item in history:

        with st.expander(
            f"{item['id']} · {item['user_question'][:75]}"
        ):

            st.caption(
                f"Executed at: {item['executed_at']}"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Execution Time",
                f"{item['execution_time']:.4f}s"
            )

            col2.metric(
                "Rows Returned",
                item["rows_returned"]
            )

            st.markdown("**Generated SQL**")

            st.code(
                item["generated_sql"],
                language="sql"
            )

            # Reuse query
            if st.button(
                "↗ Reuse This Query",
                key=f"reuse_{item['id']}"
            ):

                st.session_state["generated_sql"] = (
                    item["generated_sql"]
                )

                st.session_state["last_question"] = (
                    item["user_question"]
                )

                st.session_state.pop(
                    "query_result", None
                )

                st.success(
                    "Query loaded! Open AI SQL Assistant "
                    "to review and execute it."
                )

            # Delete query
            if st.button(
                "🗑 Delete Record",
                key=f"delete_{item['id']}"
            ):

                try:

                    deleted = delete_query_history(
                        item["id"]
                    )

                    if deleted:

                        st.success(
                            "History record deleted."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "History record was not found."
                        )

                except Exception as error:

                    st.error(
                        f"Deletion failed: {error}"
                    )
