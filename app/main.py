import streamlit as st

from app.ui.dashboard import render_dashboard
from app.ui.schema_explorer import render_schema_explorer
from app.ui.sql_assistant import render_sql_assistant
from app.ui.analytics_dashboard import render_analytics_dashboard
from app.services.query_history import initialize_history_table
from app.ui.query_history import render_query_history
from app.services.saved_queries import initialize_saved_queries_table
from app.ui.saved_queries import render_saved_queries
from app.ui.style import apply_custom_styles


# Page configuration
st.set_page_config(
    page_title="SQLGenPro",
    page_icon="🧠",
    layout="wide"
)

apply_custom_styles()

try:
    initialize_saved_queries_table()
except Exception as error:
    st.error(f"Saved queries initialization failed: {error}")

try:
    initialize_history_table()
except Exception as error:
    st.error(f"Query history initialization failed: {error}")


# Sidebar branding
st.sidebar.title("🧠 SQLGenPro")

st.sidebar.caption(
    "AI-Powered Database Intelligence"
)

st.sidebar.divider()


# Navigation
page_options = [
    "Dashboard",
    "Schema Explorer",
    "AI SQL Assistant",
    "Analytics Dashboard",
    "Query History",
    "Saved Queries"
]


if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Dashboard"

page = st.sidebar.radio(
    "Navigation",
    page_options,
    key="selected_page"
)

st.sidebar.divider()

st.sidebar.caption(
    "Version 0.4.0 | Development"
)


# Page routing
if page == "Dashboard":

    render_dashboard()


elif page == "Schema Explorer":

    render_schema_explorer()


elif page == "AI SQL Assistant":

    render_sql_assistant()

elif page == "Analytics Dashboard":

    render_analytics_dashboard()
    
elif page == "Query History":

    render_query_history()
    
elif page == "Saved Queries":
    
    render_saved_queries()
