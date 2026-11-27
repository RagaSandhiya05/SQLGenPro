import streamlit as st

from app.services.saved_queries import (
    save_query,
    get_saved_queries,
    update_saved_query,
    delete_saved_query
)


def render_saved_queries():

    st.title("⭐ Saved Queries")
    st.caption(
        "Your personal SQL library — store, organize, and reuse "
        "important queries."
    )

    st.divider()

    # Save a new query
    with st.expander("➕ Save a New Query", expanded=False):

        with st.form("save_query_form"):

            title = st.text_input(
                "Query Title",
                placeholder="e.g. Top Performing Customers"
            )

            description = st.text_area(
                "Description",
                placeholder="Briefly describe what this query does."
            )

            sql_query = st.text_area(
                "SQL Query",
                height=180,
                placeholder="SELECT * FROM customers;"
            )

            submitted = st.form_submit_button(
                "Save Query",
                use_container_width=True
            )

            if submitted:

                if not title.strip() or not sql_query.strip():
                    st.warning(
                        "Please provide both a title and SQL query."
                    )

                else:
                    try:
                        save_query(
                            title=title.strip(),
                            description=description.strip(),
                            sql_query=sql_query.strip()
                        )

                        st.success("Query saved successfully!")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Unable to save query: {error}")

    st.divider()

    # Search saved queries
    search_term = st.text_input(
        "🔍 Search Saved Queries",
        placeholder="Search by title, description, or SQL..."
    )

    try:
        saved_queries = get_saved_queries(search_term.strip() or None)

    except Exception as error:
        st.error(f"Unable to load saved queries: {error}")
        return

    if not saved_queries:
        st.info("No saved queries found. Save your first SQL query above.")
        return

    st.subheader(f"Your Library ({len(saved_queries)} queries)")

    for item in saved_queries:

        with st.expander(f"⭐ {item['title']}"):

            st.write(
                item["description"] or "No description provided."
            )

            st.caption(
                f"Created: {item['created_at']} | "
                f"Updated: {item['updated_at']}"
            )

            st.code(item["sql_query"], language="sql")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "📥 Reuse Query",
                    key=f"reuse_{item['id']}",
                    use_container_width=True
                ):
                    st.session_state["generated_sql"] = item["sql_query"]
                    st.session_state["last_question"] = (
                        f"Reused saved query: {item['title']}"
                    )
                    st.session_state.pop("query_result", None)

                    st.success(
                        "Query loaded! Navigate to AI SQL Assistant "
                        "to review and execute it."
                    )

            with col2:
                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{item['id']}",
                    use_container_width=True
                ):
                    if delete_saved_query(item["id"]):
                        st.success("Saved query deleted!")
                        st.rerun()

            st.divider()

            # Edit saved query
            with st.form(f"edit_form_{item['id']}"):

                st.markdown("**Edit Saved Query**")

                edited_title = st.text_input(
                    "Title",
                    value=item["title"],
                    key=f"title_{item['id']}"
                )

                edited_description = st.text_area(
                    "Description",
                    value=item["description"] or "",
                    key=f"description_{item['id']}"
                )

                edited_sql = st.text_area(
                    "SQL Query",
                    value=item["sql_query"],
                    height=150,
                    key=f"sql_{item['id']}"
                )

                update_clicked = st.form_submit_button(
                    "Update Query",
                    use_container_width=True
                )

                if update_clicked:

                    if not edited_title.strip() or not edited_sql.strip():
                        st.warning(
                            "Title and SQL query cannot be empty."
                        )

                    else:
                        try:
                            updated = update_saved_query(
                                query_id=item["id"],
                                title=edited_title.strip(),
                                description=edited_description.strip(),
                                sql_query=edited_sql.strip()
                            )

                            if updated:
                                st.success("Query updated successfully!")
                                st.rerun()
                            else:
                                st.warning("Saved query was not found.")

                        except Exception as error:
                            st.error(f"Unable to update query: {error}")
