import streamlit as st
from sqlalchemy import inspect, text

from app.database.connection import (
    test_connection,
    get_database_engine
)


def render_dashboard():

    # -----------------------------------
    # PAGE HEADER
    # -----------------------------------

    st.title("🧠 SQLGenPro")

    st.caption(
        "AI-Powered Database Intelligence Platform"
    )

    st.markdown(
        "Transform natural language into SQL, "
        "explore databases, and discover insights "
        "through AI-powered intelligence."
    )

    st.divider()

    # -----------------------------------
    # SYSTEM OVERVIEW
    # -----------------------------------

    st.subheader("⚡ System Overview")

    engine = None
    inspector = None
    connected = False
    table_names = []

    try:
        engine = get_database_engine()
        connected = test_connection()

        if connected:
            inspector = inspect(engine)
            table_names = inspector.get_table_names()

    except Exception as error:
        st.error(f"Database initialization failed: {error}")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.metric(
            "Database Status",
            "Connected" if connected else "Disconnected"
        )

    with col2:
        st.metric(
            "Database Tables",
            len(table_names) if connected else "—"
        )

    with col3:
        st.metric(
            "AI Engine",
            "Groq Integrated"
        )

    if connected:
        st.success(
            "PostgreSQL connection established successfully!"
        )
    else:
        st.error(
            "Unable to connect to PostgreSQL. "
            "Check your Docker container and .env configuration."
        )

    st.divider()

    # -----------------------------------
    # PLATFORM MODULES
    # -----------------------------------

    st.subheader("🚀 Platform Modules")

    st.caption(
        "Explore the core intelligence capabilities available in SQLGenPro."
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        with st.container(border=True, height=190):
            st.markdown("### 🤖 AI SQL Assistant")

            st.write(
                "Convert natural language questions into "
                "PostgreSQL queries using Groq LLM."
            )

            st.caption(
                "Natural Language • SQL Generation • Validation"
            )

        with st.container(border=True, height=190):
            st.markdown("### 📊 Analytics Dashboard")

            st.write(
                "Explore query results through interactive "
                "visualizations and AI-generated insights."
            )

            st.caption(
                "Charts • Data Analysis • AI Insights"
            )

    with col2:

        with st.container(border=True, height=190):
            st.markdown("### 🗂️ Schema Explorer")

            st.write(
                "Explore database tables, columns, relationships "
                "and schema information."
            )

            st.caption(
                "PostgreSQL • Schema Intelligence • ERD"
            )

        with st.container(border=True, height=190):
            st.markdown("### 📚 Query Management")

            st.write(
                "Maintain your SQL workflow with persistent "
                "query history and reusable saved queries."
            )

            st.caption(
                "Query History • Search • Saved Queries"
            )

    st.divider()

    # -----------------------------------
    # DATABASE OVERVIEW
    # -----------------------------------

    st.subheader("🗄️ Database Overview")

    if connected:

        st.markdown("**Available Database Tables**")

        if table_names:

            st.dataframe(
                {"Table Name": table_names},
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"SQLGenPro currently detects "
                f"{len(table_names)} database tables."
            )

        else:
            st.info(
                "No tables found in the connected database."
            )

        st.divider()

        # -----------------------------------
        # DATABASE STATISTICS
        # -----------------------------------

        st.subheader("📈 Database Statistics")

        if inspector.has_table("users"):

            try:
                with engine.connect() as connection:
                    result = connection.execute(
                        text("SELECT COUNT(*) FROM users")
                    )
                    user_count = result.scalar()

                col1, col2 = st.columns(2, gap="large")

                col1.metric("Total Users", user_count)
                col2.metric("Total Tables", len(table_names))

            except Exception as error:
                st.warning(
                    f"Unable to retrieve database statistics: {error}"
                )

        else:
            st.info(
                "A users table is not available in this database."
            )

    st.divider()

    # -----------------------------------
    # PLATFORM CAPABILITIES
    # -----------------------------------

    st.subheader("✨ Built for Intelligent Data Access")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            **🤖 AI Intelligence**

            - Groq-powered natural language processing
            - Natural Language to SQL generation
            - AI-powered data insights
            """
        )

    with col2:
        st.markdown(
            """
            **📊 Database Intelligence**

            - PostgreSQL schema discovery
            - SQL safety validation
            - Interactive analytics
            - Persistent query management
            """
        )

    st.divider()

    st.caption(
        "SQLGenPro | AI-Powered Database Intelligence | Version 0.4.0"
    )
