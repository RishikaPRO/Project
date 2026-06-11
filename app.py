import streamlit as st
 
 
class ADToolsApp:
 
    def __init__(self):
        st.set_page_config(
            page_title="AD-Tools",
            page_icon="🛠️",
            layout="wide",
            initial_sidebar_state="expanded"
        )
 
        self.initialize_session()
 
    def initialize_session(self):
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
 
        if "role" not in st.session_state:
            st.session_state.role = None
 
        if "username" not in st.session_state:
            st.session_state.username = ""
 
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
 
    def show_sidebar(self):
        with st.sidebar:
            st.markdown("## 🛠️ AD-Tools")
            st.markdown(
                f"**{st.session_state.get('team', 'AD_Tools Team')}**"
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
                st.rerun()
 
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
 
    def run(self):
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