import streamlit as st

DASHBOARD_GLOBAL_STYLES = """<style>
[data-testid="stAppViewContainer"], body, .stApp {
    background-color: #070b14 !important;
}
[data-testid="stMain"] {
    padding: 0rem !important;
    margin: 0rem !important;
}
[data-testid="stMain"] div.block-container {
    padding: 0rem !important;
    max-width: 100% !important;
    width: 100% !important;
}
[data-testid="stSidebar"] {
    background-color: #070b14 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}
[data-testid="stHeader"] {
    background-color: transparent !important;
    box-shadow: none !important;
    height: 0px;
}
[data-testid="stSidebarCollapseButton"] {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 999999 !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.1) !important;
}
[data-testid="stSidebarCollapseButton"] button {
    color: #070b14 !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
    border: none !important;
    border-radius: 10px !important;
}
[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarCollapseButton"] button:focus {
    background-color: rgba(119, 119, 119, 0.32) !important;
    color: #f8fafc !important;
}
footer {
    visibility: hidden !important;
}
iframe {
    border: none !important;
    width: 100% !important;
    display: block !important;
}
</style>"""


def inject_dashboard_page_styles():
    st.markdown(DASHBOARD_GLOBAL_STYLES, unsafe_allow_html=True)
