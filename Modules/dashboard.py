import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from styles import load_css


class EmployeeDashboard:
    def __init__(self):
        self.file_path = "dashboard.xlsx"
        self.employee_df = pd.DataFrame()
        self.leave_df = pd.DataFrame()
        self.projects_df = pd.DataFrame()

        self.load_data()

    def load_data(self):
        try:
            if not Path(self.file_path).exists():
                st.error(f"File not found: {self.file_path}")
                st.stop()
            self.employee_df = pd.read_excel(self.file_path,sheet_name="Employee")

            self.leave_df = pd.read_excel(self.file_path,sheet_name="Leave")
            self.projects_df = pd.read_excel(self.file_path,sheet_name="Job_list")
            self.employee_df.fillna("", inplace=True)
            self.leave_df.fillna(0, inplace=True)
            self.projects_df.fillna("", inplace=True)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()

    def get_total_leave_month(self):
        if "Leaves This Month" in self.leave_df.columns:
            return self.leave_df["Leaves This Month"].sum()
        return 0

    def get_total_leave_year(self):
        if "Leaves This Month.1" in self.leave_df.columns:
            return self.leave_df["Leaves This Month.1"].sum()
            
        return 0

    def get_employee_leave(self, employee_name):
        try:
            leave_row = self.leave_df[self.leave_df["Name"].astype(str).str.strip().str.lower()== employee_name.strip().lower()]
            if leave_row.empty:
                return {
                    "month": 0,
                    "year": 0,
                    "remaining": 0
                }
            month_leave = leave_row["Leaves This Month"].iloc[0]
            year_leave = leave_row["Leaves This Month.1"].iloc[0]
            return {
                "month": month_leave,
                "year": year_leave,
                "remaining": max(24 - year_leave, 0)
            }
        except Exception:
            return {
                "month": 0,
                "year": 0,
                "remaining": 0
            }
    def get_employee_projects(self, employee_name):
        try:
            return self.projects_df[self.projects_df["Team Members"].astype(str).str.contains(employee_name, case=False, na=False)]
        except Exception:
            return pd.DataFrame()
    def create_metrics(self):
        total_employees = len(self.employee_df)
        total_projects = len(self.projects_df)
        total_leave_month = self.get_total_leave_month()
        total_leave_year = self.get_total_leave_year()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Employees",total_employees)
        with col2:
            st.metric("Total Projects",total_projects)
        with col3:
            st.metric("Leave This Month",int(total_leave_month))
        with col4:
            st.metric("Leave This Year",round(total_leave_year, 1))

    def create_charts(self):

        st.subheader("Analytics")
        c1,c2= st.columns(2)
        with c1:
            dept_fig = px.pie(self.employee_df,names="Department",title="Department Distribution")
            st.plotly_chart(dept_fig, use_container_width=True)
        with c2:
            project_fig = px.pie(self.projects_df,names="Job Status",title="Project Status Distribution")
            st.plotly_chart(project_fig,use_container_width=True)

    def employee_directory(self):
        st.subheader("Employee Directory")
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("Search Employee")
        with col2:
            departments = ["All"] + sorted(self.employee_df["Department"] .astype(str).unique().tolist())
            department_filter = st.selectbox("Department",departments)
        filtered_df = self.employee_df.copy()
        if search:
            filtered_df = filtered_df[filtered_df["Name"].astype(str).str.contains(search, case=False, na=False)]
        if department_filter != "All":
            filtered_df = filtered_df[filtered_df["Department"]== department_filter]
        directory_data = []
        for _, row in filtered_df.iterrows():
            emp_name = row["Name"]
            leave_info = self.get_employee_leave(emp_name)
            projects = self.get_employee_projects(emp_name)
            directory_data.append({
                "Employee Name": emp_name,
                "Department": row["Department"],
                "Role": row["Role"],
                "Projects Assigned": len(projects),
                "Leave This Month": leave_info["month"]
            })
        st.dataframe(pd.DataFrame(directory_data),use_container_width=True,hide_index=True)
        st.divider()
        for _, employee in filtered_df.iterrows():
            self.show_employee_details(employee)
    def show_employee_details(self, employee):
        employee_name = employee["Name"]
        leave_info = self.get_employee_leave(employee_name)
        employee_projects = self.get_employee_projects(employee_name)
        with st.expander(f"{employee_name}",expanded=False):
            st.markdown("### Employee Information")
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Employee ID:** {employee['Employe ID']}" )
                st.write(f"**Username:** {employee['Username']}")
                st.write(f"**Department:** {employee['Department']}")
                st.write(f"**Role:** {employee['Role']}")

            with c2:
                st.write(f"**DOB:** {employee['DOB']}" )
                st.write(f"**Date of Joining:** {employee['Date of Joining']}")
                st.write(f"**Email:** {employee['Email']}")
                st.write( f"**Phone Number:** {employee['Phone no']}")
            st.divider()
            st.markdown("### Leave Information")
            l1, l2, l3 = st.columns(3)
            l1.metric("Leave This Month",leave_info["month"])
            l2.metric( "Leave This Year",leave_info["year"])
            l3.metric("Leave Remaining",leave_info["remaining"])
            st.divider()
            st.markdown("### Project Information")
            st.metric("Total Projects Assigned", len(employee_projects))
            if employee_projects.empty:
                st.info("No projects assigned.")
            else:
                for _, project in employee_projects.iterrows():
                    st.markdown( f"#### {project['Project Name']}")
                    p1, p2 = st.columns(2)
                    with p1:
                        st.write(f"**Project ID:** {project['Project ID']}")
                        st.write(f"**Project Type:** {project['Project Type']}")
                        st.write(f"**Project Team:** {project['Project Team']}")
                        st.write(f"**Language:** {project['Language']}")
                    with p2:
                        st.write( f"**Team Members:** {project['Team Members']}")
                        st.write(f"**Job Status:** {project['Job Status']}")
                        st.write(f"**Start Date:** {project['Start Date']}")
                        st.write(f"**Release Date:** {project['Release Date']}")
                    st.divider()
    def run(self):
        load_css()
        st.markdown("""
        <div style='
        padding:20px;
            border-radius:12px;
            background:linear-gradient(90deg,#0f172a,#1e293b);
            color:white;
            margin-bottom:20px;
        '>
    <h2 style='margin:0;'>Dashboard</h2>
        </div>
                    """, unsafe_allow_html=True)
        st.set_page_config(page_title="Employee Dashboard",layout="wide")
        st.container()
        self.create_metrics()
        st.divider()
        self.create_charts()
        st.divider()
        self.employee_directory()

def show_dashboard():
    EmployeeDashboard().run()
