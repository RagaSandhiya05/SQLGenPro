import streamlit as st

def apply_custom_styles():

    st.markdown(
        """
        <style>

        /* Main application */
        .stApp {
            background-color: #0B1120;
            color: #E2E8F0;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        /* Headings */
        h1, h2, h3 {
            color: #F8FAFC !important;
            font-weight: 650 !important;
        }

        p, label, span {
            color: #CBD5E1;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #253047;
        }

        section[data-testid="stSidebar"] h1 {
            color: #A5B4FC !important;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background-color: #151F32;
            border: 1px solid #27364F;
            padding: 18px;
            border-radius: 12px;
        }

        div[data-testid="stMetricLabel"] {
            color: #94A3B8;
        }

        div[data-testid="stMetricValue"] {
            color: #A5B4FC;
            font-weight: 700;
        }

        /* Buttons */
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 9px;
            border: 1px solid #394967;
            background-color: #1E293B;
            color: #E2E8F0;
            font-weight: 600;
            transition: 0.2s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: #818CF8;
            color: #C7D2FE;
            background-color: #263653;
        }

        /* Input fields */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox div[data-baseweb="select"] {
            background-color: #151F32;
            color: #E2E8F0;
            border-radius: 8px;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #151F32;
            border-radius: 8px;
            color: #E2E8F0;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border: 1px solid #27364F;
            border-radius: 10px;
            overflow: hidden;
        }

        /* Dividers */
        hr {
            border-color: #27364F;
        }

        /* Alerts */
        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Streamlit top toolbar */
        header[data-testid="stHeader"] {
            background-color: #0B1120;
        }

        /* SQL and Python code blocks */
        div[data-testid="stCode"] pre {
            background-color: #151F32 !important;
            border: 1px solid #334155;
            border-radius: 10px;
        }

        div[data-testid="stCode"] code {
            color: #E2E8F0 !important;
        }

        /* Success alerts */
        div[data-testid="stAlert"][kind="success"] {
            background-color: #123329 !important;
            border: 1px solid #16634A;
        }

        div[data-testid="stAlert"][kind="success"] p {
            color: #BBF7D0 !important;
        }

        /* Info alerts */
        div[data-testid="stAlert"][kind="info"] {
            background-color: #172B46 !important;
            border: 1px solid #315A89;
        }

        div[data-testid="stAlert"][kind="info"] p {
            color: #BFDBFE !important;
        }

        /* Warning alerts */
        div[data-testid="stAlert"][kind="warning"] {
            background-color: #3B2D17 !important;
            border: 1px solid #926B25;
        }

        div[data-testid="stAlert"][kind="warning"] p {
            color: #FDE68A !important;
        }

        /* Sidebar radio controls */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            color: #CBD5E1 !important;
        }

        /* Smooth visual transitions */
        .stButton > button,
        .stDownloadButton > button {
            transition: all 0.2s ease-in-out;
        }

        /* Top toolbar */
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"] {
            background-color: #0B1120 !important;
        }

        /* Success notification */
        div[data-testid="stAlert"] {
            background-color: #123329 !important;
            border: 1px solid #16634A !important;
            border-radius: 10px;
        }

        div[data-testid="stAlert"] p {
            color: #BBF7D0 !important;
        }

        /* Professional sidebar navigation */
        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 8px;
        }

        /* Navigation items */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            padding: 10px 12px;
            border-radius: 9px;
            transition: all 0.2s ease;
        }

        /* Hover effect */
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: #1E293B;
        }

        /* Selected navigation item */
        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background-color: #263653;
            border: 1px solid #818CF8;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
