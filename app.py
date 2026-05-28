import streamlit as st
import pandas as pd
# Page configuration
st.set_page_config(page_title="AD-TOOLS", page_icon="🔐", layout="wide",initial_sidebar_state="expanded")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in =False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""
if not st.session_state.logged_in:
    from pages.login import showlogin
    showlogin()
else:
    from utils.sidebar import showsidebar
    page=showsidebar()
    if page=="Dashboard":
        from pages.dashboard import show_dashboard 
        show_dashboard()
    elif page=="Employee Details":
        from pages.employee_details import show_employee_details
        show_employee_details()
    elif page=="Job List":
        from pages.job_list import show_job_list
        show_job_list()
    elif page=="Audit Work":
        from pages.audit_work import show_audit_work
        show_audit_work()
    elif page=="Reports":
        from pages.reports import show_reports
        show_reports()
    elif page=="Statusmail/Leave":
        from pages.statusmail_leave import show_statusmailleave
        show_statusmailleave()

