import base64
import streamlit as st
from pathlib import Path
 
 
class ADToolsApp:
 
    def __init__(self):
        st.set_page_config(
            page_title="Gunma-WorkVista",
            #page_icon="🛠️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
 
        self.initialize_session()
    #Initialise session 
    def initialize_session(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
 
        if "role" not in st.session_state:
            st.session_state.role = None
 
        if "username" not in st.session_state:
            st.session_state.username = ""
 
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
    #Shows left sidebar menu options
    def show_sidebar(self):
        with st.sidebar:
            st.markdown(
                '<h2 style="color:#9b5cff; margin-bottom: 0.25rem;">Gunma-WorkVista</h2>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div style="color:#9b5cff; font-weight:700;">{st.session_state.get("team", "AD_Tools Team")}</div>',
                unsafe_allow_html=True
            )
            st.markdown("---")
 
            pages = [
                "Dashboard",
                "Employee Details",
                "Job List",
                "Audit",
                "Reports",
                "Statusmail/Leave"
            ]
 
            icons = ["", "", "", "", "", ""]
 
            for icon, page in zip(icons, pages):
                if st.button(
                    f"{icon} {page}",
                    key=f"nav_{page}",
                    use_container_width=True
                ):
                    st.session_state.current_page = page
                    st.rerun()
 
            st.markdown("---")
            st.markdown(
                f"**{st.session_state.get('username', '').title()}**"
            )
            st.markdown(
                f"_{st.session_state.get('role', '')}_"
            )
 
            if st.button("Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                    st.success("Logout successfull!")
                st.rerun()
    # Load the Dashboard
    def load_page(self):
        page = st.session_state.current_page
 
        if page == "Dashboard":
            from Modules.dashboard import show_dashboard
            show_dashboard()
 
        elif page == "Employee Details":
            from Modules.employee_details import show_employee_details
            show_employee_details()
 
        elif page == "Job List":
            from Modules.job_list import show_job_list
            show_job_list()
 
        elif page == "Audit":
            from Modules.audit_work import show_audit
            show_audit()
 
        elif page == "Reports":
            from Modules.reports import show_reports
            show_reports()
 
        elif page == "Statusmail/Leave":
            from Modules.statusmail_leave import show_statusmail
            show_statusmail()
 
    def show_logo(self):
        logo_path = Path(__file__).parent / "logo.jpeg"
        if logo_path.exists():
            st.markdown("<style>.logo-image img{border-radius:12px;}</style>", unsafe_allow_html=True)
            cols = st.columns([7, 1])
            with cols[1]:
                st.image(str(logo_path), width=120)
        else:
            st.warning("logo.jpeg not found in the project folder.")
 
    def run(self):
        self.show_logo()
        if not st.session_state.logged_in:
            from Modules.login import show_login
            show_login()
        else:
            self.show_sidebar()
            self.load_page()
 
 
def main():
    app = ADToolsApp()
    app.run()
 
 
if __name__ == "__main__":
    main()