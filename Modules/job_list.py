#####Reporting Manager#####

#insert values
#View added values in table
#view Graphical representation of progress
#Edit values and update progress
#Delete values

import streamlit as st
import pandas as pd
import altair as alt
import os
import uuid
from datetime import datetime
from openpyxl import Workbook


def show_job_list():
    st.set_page_config(page_title="Job Tracker", layout="wide")
    filename = "job_tracker.xlsx"
    expected_columns = ["Record ID","Project ID","Project Name", "Employee ID", "Employee Name", "Job Undertaken", "Time Duration", "Progress", "Last Updated"]

    # Create Excel file if it doesn't exist
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Job Tracker"
        ws.append(expected_columns)
        wb.save(filename)

    # Load data
    df = pd.read_excel(filename)

    # Check if all expected columns exist, if not recreate the file
    if not all(col in df.columns for col in expected_columns):
        os.remove(filename)
        wb = Workbook()
        ws = wb.active
        ws.title = "Job Tracker"
        ws.append(expected_columns)
        wb.save(filename)
        df = pd.read_excel(filename)

    # Project selection
    if "project_selected" not in st.session_state:
        st.session_state.project_selected = False
    if not st.session_state.project_selected:
        st.title("Open Project")
        with st.form("project_form"):
            st.subheader("Select Project")
            project_id = st.text_input("Project ID")
            project_name = st.text_input("Project Name")
            start_button = st.form_submit_button("Open Project")
            if start_button:
                st.session_state.project_id = project_id
                st.session_state.project_name = project_name
                st.session_state.project_selected = True
                st.rerun()
        st.stop()

    # Main page
    project_id = st.session_state.project_id
    project_name = st.session_state.project_name
    st.title("Job Tracker Application")
    st.markdown(f"# Project : {project_name}")
    st.markdown(f"### Project ID : {project_id}")
    st.divider()
    project_df = df[df["Project ID"].astype(str) == str(project_id)]
    tab1, tab2 = st.tabs(["Add Entry", "Dashboard"])

    # Add Entry
    with tab1:
        st.subheader("Add Employee Job Details")
        with st.form("add form", clear_on_submit=True):
            emp_id = st.text_input("Employee ID")
            emp_name = st.text_input("Employee Name")
            job = st.selectbox("Job Undertaken", ["Requirement Document","Design Document","Coding","ITP","Testing","Audit Work"])
            duration = st.text_input("Time Duration")
            progress = st.slider("Progress", 0, 100, 0)
            add_btn = st.form_submit_button("Save")
            if add_btn:
                new_row = {
                    "Record ID": str(uuid.uuid4()),
                    "Project ID": project_id,
                    "Project Name": project_name,
                    "Employee ID": emp_id,
                    "Employee Name": emp_name,
                    "Job Undertaken": job,
                    "Time Duration": duration,
                    "Progress": progress,
                    "Last Updated": datetime.now(),
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_excel(filename, index=False)
                st.success("Data Saved Successfully")
                st.rerun()

    # Dashboard
    with tab2:
        df = pd.read_excel(filename)
        project_df = df[df["Project ID"].astype(str) == str(project_id)]
        if not project_df.empty:
            project_df = project_df.sort_values(by=["Employee ID", "Employee Name"])

        st.subheader("Employee Records")
        if project_df.empty:
            st.info("No records available for this project.")
        else:
            for _, row in project_df.iterrows():
                col1, col2, col3, col4 = st.columns([4, 2, 1, 1])
                with col1:
                    st.write(f"**{row['Employee Name']}** ({row['Employee ID']})")
                    st.write(row["Job Undertaken"])
                with col2:
                    st.write(f"{row['Progress']}%")
                with col3:
                    if st.button("Edit", key=f"edit_{row['Record ID']}"):
                        st.session_state.edit_record = row["Record ID"]
                with col4:
                    if st.button("Delete", key=f"delete_{row['Record ID']}"):
                        df = df[df["Record ID"] != row["Record ID"]]
                        df.to_excel(filename, index=False)
                        st.success("Record Deleted")
                        st.rerun()

            st.divider()
            # Edit section
            if "edit_record" in st.session_state:
                record_id = st.session_state.edit_record
                edit_row = df[df["Record ID"] == record_id]
                if not edit_row.empty:
                    edit_row = edit_row.iloc[0]
                    st.subheader("Edit Record")
                    with st.form("edit_form"):
                        new_job = st.selectbox(
                            "Job Undertaken",
                            ["Requirement Document", "Design Document", "Coding", "ITP", "Testing", "Audit Work"],
                            index=["Requirement Document", "Design Document", "Coding", "ITP", "Testing", "Audit Work"].index(edit_row["Job Undertaken"]),
                        )
                        new_duration = st.text_input("Time Duration", value=str(edit_row["Time Duration"]))
                        new_progress = st.slider("Progress", 0, 100, int(edit_row["Progress"]))
                        update_btn = st.form_submit_button("Update")
                        if update_btn:
                            df.loc[df["Record ID"] == record_id, "Time Duration"] = new_duration
                            df.loc[df["Record ID"] == record_id, "Progress"] = new_progress
                            df.loc[df["Record ID"] == record_id, "Job Undertaken"] = new_job
                            df.loc[df["Record ID"] == record_id, "Last Updated"] = datetime.now()
                            df.to_excel(filename, index=False)
                            del st.session_state.edit_record
                            st.success("Record Updated")
                            st.rerun()

            st.divider()
            st.subheader("Employee Progress Tracking")
            employee_groups = project_df.groupby("Employee ID")
            for emp_id, emp_data in employee_groups:
                emp_name = emp_data.iloc[0]["Employee Name"]
                st.markdown(f"### Employee : {emp_name} ({emp_id})")
                for _, row in emp_data.iterrows():
                    col1, col2 = st.columns([3, 3])
                    with col1:
                        st.write(f"**{row['Job Undertaken']}**")
                        st.write(f"Duration : {row['Time Duration']}")
                    with col2:
                        st.progress(int(row["Progress"]))
                        st.write(f"{row['Progress']}% Completed")
                st.divider()

            st.subheader("Progress Visualization")
            chart = alt.Chart(project_df).mark_bar().encode(
                x=alt.X("Employee Name:N", title="Employee"),
                y=alt.Y("Progress:Q", title="Progress %"),
                color="Job Undertaken:N",
                tooltip=["Employee Name", "Employee ID", "Job Undertaken", "Progress"],
            ).properties(height=450)
            st.altair_chart(chart, use_container_width=True)

    st.divider()
    if st.button("Open Another Project"):
        st.session_state.project_selected = False
        if "edit_record" in st.session_state:
            del st.session_state.edit_record
        st.rerun()
