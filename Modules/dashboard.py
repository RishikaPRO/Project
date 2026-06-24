import json
from pathlib import Path
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from Modules.dashboard_layout import inject_dashboard_page_styles
from Modules.dashboard_template import build_dashboard_html


class DashboardPage:
    """Encapsulates dashboard logic, data loading, and rendering."""

    FILE = "dashboard.xlsx"

    @staticmethod
    @st.cache_data
    def load_data(fp):
        """Load Excel sheets used by the dashboard."""
        if not Path(fp).exists():
            return None, None, None

        try:
            employees = pd.read_excel(fp, sheet_name="Employee").fillna("")
            leaves = pd.read_excel(fp, sheet_name="Leave").fillna(0)
            jobs = pd.read_excel(fp, sheet_name="Job_list").fillna("")
            return employees, leaves, jobs
        except Exception as ex:
            st.error(f"Error reading Excel sheets: {ex}")
            return None, None, None

    @staticmethod
    def emp_leave(ldf, name):
        """Return leave summary for a single employee."""
        row = ldf[ldf["Name"].astype(str).str.strip().str.lower() == name.strip().lower()]
        if row.empty:
            return {"month": 0, "year": 0, "remaining": 24}

        month_leaves = float(row["Leaves This Month"].iloc[0]) if "Leaves This Month" in ldf.columns else 0
        year_leaves = float(row["Leaves This Month.1"].iloc[0]) if "Leaves This Month.1" in ldf.columns else 0
        return {"month": month_leaves, "year": year_leaves, "remaining": max(24 - year_leaves, 0)}

    @staticmethod
    def emp_projs(pdf, name):
        """Return projects that include the employee in team members."""
        return pdf[pdf["Team Members"].astype(str).str.contains(name, case=False, na=False)]

    @staticmethod
    def build_json(edf, ldf, pdf, role, uname):
        """Build the dashboard data payload for the HTML template."""
        palette = ["#4f8dff", "#7c5cff", "#00e5cc", "#ffb432", "#ff6b9d", "#ff8c55", "#a78bfa", "#34d399"]
        status_colors = {
            "In Progress": "#00e5cc",
            "Completed": "#4f8dff",
            "On Hold": "#ffb432",
            "Review": "#7c5cff",
        }
        status_progress = {
            "Completed": 100,
            "Review": 85,
            "In Progress": 50,
            "On Hold": 25,
        }

        employees = []
        for idx, (_, row) in enumerate(edf.iterrows()):
            name = str(row.get("Name", "")).strip()
            if not name or (role == "team member" and str(row.get("Username", "")).strip().lower() != uname):
                continue

            leave_summary = DashboardPage.emp_leave(ldf, name)
            employees.append({
                "name": name,
                "role": str(row.get("Role", "")),
                "dept": str(row.get("Department", "")),
                "empId": str(row.get("Employe ID", "")),
                "username": str(row.get("Username", "")),
                "dob": str(row.get("DOB", "")),
                "joined": str(row.get("Date of Joining", "")),
                "email": str(row.get("Email", "")),
                "phone": str(row.get("Phone no", "")),
                "projects": len(DashboardPage.emp_projs(pdf, name)),
                "leaveMonth": round(leave_summary["month"], 1),
                "leaveYear": round(leave_summary["year"], 1),
                "leaveRemaining": round(leave_summary["remaining"], 1),
                "active": leave_summary["month"] == 0,
                "color": palette[idx % len(palette)],
            })

        projects = []
        for _, row in pdf.iterrows():
            status = str(row.get("Job Status", "")).strip()
            members = str(row.get("Team Members", ""))
            initials = [
                "".join(part.strip()[0].upper() for part in member.split() if member.strip())
                for member in members.split(",")
                if member.strip()
            ][:4]
            projects.append({
                "name": str(row.get("Project Name", "")),
                "id": str(row.get("Project ID", "")),
                "type": str(row.get("Project Type", "")),
                "team": str(row.get("Project Team", "")),
                "members": members,
                "teamInitials": initials,
                "lang": str(row.get("Language", "")),
                "status": status,
                "start": str(row.get("Start Date", "")),
                "release": str(row.get("Release Date", "")),
                "pct": status_progress.get(status, 40),
                "color": status_colors.get(status, "#4f8dff"),
            })

        leaves_month = float(ldf["Leaves This Month"].sum()) if "Leaves This Month" in ldf.columns else 0
        leaves_year = float(ldf["Leaves This Month.1"].sum()) if "Leaves This Month.1" in ldf.columns else 0

        return {
            "metrics": {
                "totalEmployees": len(edf),
                "totalProjects": len(pdf),
                "leaveThisMonth": round(leaves_month, 1),
                "leaveThisYear": round(leaves_year, 1),
            },
            "employees": employees,
            "projects": projects,
            "deptCounts": edf["Department"].value_counts().to_dict() if "Department" in edf.columns else {},
            "projStatus": pdf["Job Status"].value_counts().to_dict() if "Job Status" in pdf.columns else {},
            "role": role,
        }

    def show(self):
        """Render the dashboard using current Streamlit session data."""
        role = st.session_state.get("role", "reporting manager").strip().lower()
        username = st.session_state.get("Username", "").strip().lower()
        display_name = st.session_state.get("display_name", "User")
        initials = "".join(part[0].upper() for part in display_name.split() if part)[:2] or "JD"

        employees, leaves, jobs = DashboardPage.load_data(self.FILE)
        if employees is None:
            st.error(f"Could not load **{self.FILE}**. Ensure sheets match exactly: Employee, Leave, Job_list")
            return

        dashboard_data = DashboardPage.build_json(employees, leaves, jobs, role, username)
        html = build_dashboard_html(dashboard_data, initials)

        inject_dashboard_page_styles()
        components.html(html, height=1200, scrolling=True)


def show_dashboard():
    """Compatibility wrapper that renders the dashboard via DashboardPage."""
    DashboardPage().show()


def main():
    """Entry point for dashboard execution."""
    st.set_page_config(page_icon="",layout="wide",initial_sidebar_state="expanded" )
    st.session_state.setdefault("role", "reporting manager")
    st.session_state.setdefault("Username", "")
    st.session_state.setdefault("display_name", "Admin User")

    dashboard = DashboardPage()
    dashboard.show()


if __name__ == "__main__":
    main()