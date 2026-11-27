import streamlit as st

from app.services.ai_insights import generate_data_insights

from app.services.analytics_engine import (
    recommend_chart,
    create_chart,
    get_column_types
)


def render_analytics_dashboard():

    st.title("📊 Analytics Dashboard")

    st.caption(
        "Explore query results through interactive "
        "visualizations and AI-powered analytics."
    )

    st.divider()

    result = st.session_state.get("query_result")

    if not result:

        st.info(
            "No query results available yet. "
            "Generate and execute a SQL query in "
            "the AI SQL Assistant first."
        )

        return

    dataframe = result["data"]

    if dataframe is None or dataframe.empty:

        st.warning(
            "The executed query returned no records."
        )

        return

    st.subheader("Database Analytics Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        len(dataframe)
    )

    col2.metric(
        "Total Columns",
        len(dataframe.columns)
    )

    col3.metric(
        "Numeric Fields",
        len(get_column_types(dataframe)["numeric"])
    )

    col4.metric(
        "Execution Time",
        f"{result['execution_time']} sec"
    )

    st.divider()


    st.subheader("✨ Smart Visualization")

    recommendation = recommend_chart(dataframe)

    st.info(
        f"Recommended Chart: "
        f"{recommendation['type'].upper()} "
        f"— {recommendation['reason']}"
    )

    chart_options = [
        "Automatic",
        "Bar",
        "Line",
        "Pie",
        "Scatter",
        "Histogram"
    ]

    selected_chart = st.selectbox(
        "Choose Visualization",
        chart_options
    )

    chart_mapping = {
        "Automatic": None,
        "Bar": "bar",
        "Line": "line",
        "Pie": "pie",
        "Scatter": "scatter",
        "Histogram": "histogram"
    }

    chart_type = chart_mapping[selected_chart]

    try:

        figure = create_chart(
            dataframe,
            chart_type
        )

        if figure is not None:

            st.plotly_chart(
                figure,
                use_container_width=True
            )

        else:

            st.warning(
                "This visualization is not suitable "
                "for the available query results."
            )

    except Exception as error:

        st.error(
            f"Chart generation failed: {error}"
        )

    st.divider()

    st.subheader("📋 Query Data Preview")

    st.dataframe(
        dataframe,
        use_container_width=True,
        hide_index=True
    )

    # Export analytics data
    st.download_button(
        label="⬇️ Download Analytics Data",
        data=dataframe.to_csv(index=False),
        file_name="sqlgenpro_analytics.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    st.subheader("🧠 AI-Powered Data Insights")

    st.caption(
        "Discover hidden patterns, identify trends, "
        "and generate actionable recommendations "
        "from your SQL query results."
    )

    if st.button(
        "✨ Generate AI Insights",
        use_container_width=True,
        type="primary"
    ):

        with st.spinner(
            "SQLGenPro AI is analyzing your data..."
        ):

            try:

                insights = generate_data_insights(dataframe)

                st.session_state["ai_insights"] = insights

                st.success(
                    "AI analysis completed successfully!"
                )

            except Exception as error:

                st.error(
                    f"Unable to generate AI insights: {error}"
                )

    # Display previously generated insights
    insights = st.session_state.get("ai_insights")

    if insights:

        st.divider()

        st.subheader("📊 AI Analysis Report")

        st.markdown(insights)

        st.download_button(
            label="📥 Download AI Insights Report",
            data=insights,
            file_name="sqlgenpro_ai_insights.md",
            mime="text/markdown",
            use_container_width=True
        )
