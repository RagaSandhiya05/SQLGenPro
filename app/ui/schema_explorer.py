import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from app.database.erd_generator import generate_erd

from app.database.schema_intelligence import (
    get_database_schema,
    get_database_relationships,
    format_schema_for_llm
)


def render_schema_explorer():


    st.title("🗄️ Database Schema Explorer")

    st.caption(
        "Explore database structures, columns and relationships "
        "through intelligent schema discovery."
    )


    try:

        schema = get_database_schema()

        relationships = get_database_relationships(schema)

        summary = {
            "total_tables": len(schema),

            "total_columns": sum(
                len(details["columns"])
                for details in schema.values()
            ),

            "total_primary_keys": sum(
                len(details["primary_keys"])
                for details in schema.values()
            ),

            "total_relationships": len(relationships)
        }

    except Exception as error:

        st.error(
            f"Unable to retrieve database schema: {error}"
        )

        return


    st.subheader("⚡ Schema Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Tables",
        summary["total_tables"]
    )

    col2.metric(
        "Columns",
        summary["total_columns"]
    )

    col3.metric(
        "Primary Keys",
        summary["total_primary_keys"]
    )

    col4.metric(
        "Relationships",
        summary["total_relationships"]
    )

    st.divider()


    st.subheader("📋 Table Explorer")

    if schema:

        selected_table = st.selectbox(
            "Select a database table",
            options=list(schema.keys())
        )

        if selected_table:

            details = schema[selected_table]

            st.markdown(
                f"### Table: `{selected_table}`"
            )

            column_data = []

            for column in details["columns"]:

                column_data.append({

                    "Column": column["name"],

                    "Data Type": column["type"],

                    "Nullable": column["nullable"],

                    "Primary Key": column["primary_key"],

                    "Foreign Key": column.get(
                        "foreign_key", False
                    ),

                    "Unique": column["unique"]

                })

            st.dataframe(
                pd.DataFrame(column_data),
                use_container_width=True,
                hide_index=True
            )

            st.write(
                "**Primary Keys:**",
                details["primary_keys"]
            )

            if details["foreign_keys"]:

                st.write("**Foreign Keys:**")

                for fk in details["foreign_keys"]:

                    source_columns = ", ".join(
                        fk["constrained_columns"] or []
                    )

                    target_columns = ", ".join(
                        fk["referred_columns"] or []
                    )

                    st.write(
                        f"- `{source_columns}` → "
                        f"`{fk['referred_table']}` "
                        f"(`{target_columns}`)"
                    )

            else:

                st.info(
                    "No foreign keys found for this table."
                )

    else:

        st.info(
            "No database tables are available to explore."
        )

    st.divider()

    st.subheader("🔗 Database Relationships")

    if relationships:

        relationship_data = []

        for relation in relationships:

            relationship_data.append({

                "Source Table": relation["source_table"],

                "Source Column": ", ".join(
                    relation["source_columns"]
                ),

                "Target Table": relation["target_table"],

                "Target Column": ", ".join(
                    relation["target_columns"]
                )

            })

        st.dataframe(
            pd.DataFrame(relationship_data),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No foreign-key relationships found "
            "in the connected database."
        )

    st.divider()


    st.subheader("🤖 AI-Ready Schema Context")

    st.caption(
        "Database metadata formatted for intelligent "
        "natural-language-to-SQL generation."
    )

    with st.expander("View generated schema context"):

        try:

            schema_context = format_schema_for_llm()

            st.code(
                schema_context,
                language="text"
            )

            st.download_button(
                label="⬇️ Download Schema Context",
                data=schema_context,
                file_name="sqlgenpro_schema.txt",
                mime="text/plain"
            )

        except Exception as error:

            st.error(
                f"Unable to generate schema context: {error}"
            )

    st.divider()

    st.subheader("🧬 Entity Relationship Diagram")

    st.caption(
        "Automatically generated from PostgreSQL "
        "tables, columns and foreign-key relationships."
    )

    if schema:

        try:

            diagram = generate_erd()

            # Render Graphviz as SVG
            svg_output = diagram.pipe(
                format="svg"
            ).decode("utf-8")

            # Display generated SVG
            components.html(
                f"""
                <div style="
                    width: 100%;
                    height: 100%;
                    overflow: auto;
                    background-color: #0B1220;
                    border-radius: 12px;
                    padding: 15px;
                    box-sizing: border-box;
                ">
                    <style>
                        svg {{
                            max-width: none;
                            height: auto;
                        }}
                    </style>

                    {svg_output}

                </div>
                """,
                height=850,
                scrolling=True
            )

            st.caption(
                f"ERD generated successfully for "
                f"{len(schema)} database tables."
            )

        except Exception as error:

            st.error(
                f"ER diagram rendering failed: {error}"
            )

            st.info(
                "Verify that Graphviz is installed and "
                "its executable is available in your system PATH."
            )

    else:

        st.info(
            "The ER diagram cannot be generated "
            "because no database tables were found."
        )

    st.divider()


    st.caption(
        "SQLGenPro | Database Schema Intelligence | Version 0.4.0"
    )
