import streamlit as st
 
def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)
 
    st.markdown("""
    <style>
 
    /* ==========================================
       APP BACKGROUND
       ========================================== */
 
    .stApp {
        background: linear-gradient(
            180deg,
            #EEF3F8 0%,
            #F8FAFC 100%
        );
    }
 
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
 
    /* ==========================================
       HEADINGS
       ========================================== */
 
    h1 {
        color: #1F4E79;
        font-weight: 700;
    }
 
    h2 {
        color: #334155;
        font-weight: 600;
    }
 
    h3 {
        color: #334155;
        font-weight: 600;
    }
 
    /* ==========================================
       KPI CARDS
       ========================================== */
 
    [data-testid="metric-container"] {
 
        background: linear-gradient(
            135deg,
            #FFFFFF,
            #F7F9FC
        );
 
        border: 1px solid #D6DEE8;
 
        border-radius: 14px;
 
        padding: 18px;
 
        box-shadow: 0px 4px 12px rgba(
            0,
            0,
            0,
            0.05
        );
    }
 
    /* ==========================================
       DATAFRAME
       ========================================== */
 
    [data-testid="stDataFrame"] {
 
        background: #FFFFFF;
 
        border: 1px solid #D6DEE8;
 
        border-radius: 14px;
 
        overflow: hidden;
 
        box-shadow: 0px 3px 10px rgba(
            0,
            0,
            0,
            0.05
        );
    }
 
    /* ==========================================
       TABS
       ========================================== */
 
    .stTabs [data-baseweb="tab"] {
 
        background: #E8EEF5;
 
        border-radius: 10px;
 
        padding: 10px 18px;
 
        margin-right: 6px;
 
        color: #1F4E79;
 
        font-weight: 600;
    }
 
    .stTabs [aria-selected="true"] {
 
        background: linear-gradient(
            135deg,
            #1F4E79,
            #2E75B6
        ) !important;
 
        color: white !important;
    }
 
    /* ==========================================
       BUTTONS
       ========================================== */
 
    .stButton button {
 
        background: linear-gradient(
            135deg,
            #1F4E79,
            #2E75B6
        );
 
        color: white;
 
        border: none;
 
        border-radius: 10px;
 
        font-weight: 600;
 
        height: 42px;
 
        box-shadow: 0px 2px 8px rgba(
            31,
            78,
            121,
            0.25
        );
    }
 
    .stButton button:hover {
 
        transform: translateY(-1px);
 
        background: linear-gradient(
            135deg,
            #163A5C,
            #1F4E79
        );
    }
 
    /* ==========================================
       TEXT INPUTS
       ========================================== */
 
    .stTextInput input {
 
        background: white;
 
        border-radius: 10px;
 
        border: 1px solid #D6DEE8;
    }
 
    /* ==========================================
       SELECTBOX
       ========================================== */
 
    .stSelectbox > div {
 
        border-radius: 10px;
    }
 
    /* ==========================================
       EXPANDERS
       ========================================== */
 
    .streamlit-expanderHeader {
 
        background: white;
 
        border-radius: 10px;
 
        border: 1px solid #D6DEE8;
 
        font-weight: 600;
    }
 
    /* ==========================================
       SUCCESS MESSAGE
       ========================================== */
 
    .stSuccess {
 
        border-radius: 10px;
    }
 
    /* ==========================================
       INFO MESSAGE
       ========================================== */
 
    .stInfo {
 
        border-radius: 10px;
    }
 
    /* ==========================================
       WARNING MESSAGE
       ========================================== */
 
    .stWarning {
 
        border-radius: 10px;
    }
 
    /* ==========================================
       SIDEBAR
       ========================================== */
 
    section[data-testid="stSidebar"] {
 
        background: linear-gradient(
            180deg,
            #1F4E79,
            #163A5C
        );
    }
 
    section[data-testid="stSidebar"] * {
 
        color: white;
    }
 
    </style>
    """, unsafe_allow_html=True)
def page_banner(title, subtitle=""):
 
    st.markdown(f"""
    <div style="
    background: linear-gradient(
        135deg,
        #1F4E79,
        #2E75B6
    );
 
    padding: 24px;
 
    border-radius: 16px;
 
    margin-bottom: 20px;
 
    color: white;
 
    box-shadow: 0px 4px 12px rgba(
        0,
        0,
        0,
        0.12
    );
    ">
 
    <h2 style="margin:0;">
        {title}
    </h2>
 
    <p style="margin-top:8px;">
        {subtitle}
    </p>
 
    </div>
    """, unsafe_allow_html=True)
 