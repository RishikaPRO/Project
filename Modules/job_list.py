import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import random
from datetime import datetime
from styles import load_css

#Manager Class for Excel Operations
class ExcelManager:
    def __init__(self, file_path):
        self.file_path = file_path
    def load_data(self):
        return pd.read_excel(self.file_path)
    def save_data(self, df):
        df.to_excel(self.file_path, index=False)

#Filter class for project data
class ProjectFilter:
    @staticmethod
    def apply_filter(df, category, value):
        mapping = {
            "Project Type": "Project_Type",
            "Project Team": "Project_Team",
            "Language": "Language",
            "Job Status": "Job_Status",
            "Employee": "Employee_Name"
        }
        if category == "All":
            return df
        return df[df[mapping[category]] == value]

#Main function of the job_list page
class JobListPage:
    @classmethod
    def show_job_list(cls):
        load_css()
        st.title("Job List")
        excel_file = "job_tracker.xlsx"
        try:
            excel = ExcelManager(excel_file)
            df = excel.load_data()
        except FileNotFoundError:
            st.error("job_tracker.xlsx not found")
            st.stop()
        except PermissionError:
            st.error("Excel file is currently open. Please close it.")
            st.stop()
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()

        # Project Selection
        st.subheader("Project Selection")
        project_ids = sorted(
            df["Project_ID"].dropna().unique())
        selected_project = st.selectbox(
            "Select Project ID",
            project_ids
        )
        project_df = df[
            df["Project_ID"] == selected_project
        ].copy()
        if project_df.empty:
            st.warning("No project data found.")
            return
        project_name = project_df[
            "Project_Name"
        ].iloc[0]
        st.text_input(
            "Project Name",
            value=project_name,
            disabled=True
        )
        
        #Filters for project data display
        st.subheader("Filters")
        filter_category= st.selectbox(
            "Filter By",
            [
                "All",
                "Project Type",
                "Project Team",
                "Language",
                "Job Status",
                "Employee"
            ]
        )
        filtered_df = project_df.copy()
        if filter_category != "All":
            column_mapping = {
                "Project Type": "Project_Type",
                "Project Team": "Project_Team",
                "Language": "Language",
                "Job Status": "Job_Status",
                "Employee": "Employee_Name"
            }
            selected_column = column_mapping[
                filter_category
            ]
            value = st.selectbox(
                f"Select {filter_category}",
                sorted( project_df[selected_column].dropna().unique()))
            filtered_df = ProjectFilter.apply_filter(project_df, filter_category, value )
        
        #Employee Table
        st.subheader("Employee Details")
        editable_columns = ["Project_ID","Project_Name","Employee_Name","Project_Type","Project_Team","Language","Job_Undertaken","Job_Status","Start_Date","End_Date"]
        editable_df = filtered_df[
            editable_columns
        ].copy()

        header_cols = st.columns([1] * len(editable_columns) + [0.7])
        for col_obj, col_name in zip(header_cols[:-1], editable_columns):
            col_obj.markdown(f"**{col_name}**")
        header_cols[-1].markdown("**Edit**")

        if "edit_record" not in st.session_state:
            st.session_state.edit_record = None

        for row_index, row in editable_df.iterrows():
            row_cols = st.columns([1] * len(editable_columns) + [0.7])
            for col_obj, col_name in zip(row_cols[:-1], editable_columns):
                col_obj.write(row[col_name])
            if row_cols[-1].button("Edit", key=f"edit_{row_index}"):
                st.session_state.edit_record = row_index

            if st.session_state.edit_record == row_index:
                with st.expander("Edit this row", expanded=True):
                    with st.form(f"edit_form_{row_index}"):
                        new_values = {}
                        for field in editable_columns:
                            if field == "Job_Undertaken":
                                options = ["Requirement Document", "Design Document", "Coding", "ITP", "Testing", "Audit Work"]
                                selected_index = 0
                                try:
                                    selected_index = options.index(str(row[field]))
                                except ValueError:
                                    selected_index = 0
                                new_values[field] = st.selectbox(
                                    "Job Undertaken",
                                    options,
                                    index=selected_index,
                                    key=f"job_{row_index}"
                                )
                            else:
                                new_values[field] = st.text_input(field, value=str(row[field]), key=f"{field}_{row_index}")
                        update_btn = st.form_submit_button("Update")

                        if update_btn:
                            for field, value in new_values.items():
                                df.loc[row_index, field] = value
                            df.loc[row_index, "Last Updated"] = datetime.now()
                            excel.save_data(df)
                            st.success("Row updated and saved to Excel.")
                            st.session_state.edit_record = None
                            st.experimental_rerun()
            else:
                st.session_state.edit_record = None

        #Save changes to Excel
        st.markdown("---")
        if st.button("Save All Changes"):
            try:
                updated_project_df = editable_df.copy()
                remaining_df = df[df["Project_ID"] != selected_project]
                final_df = pd.concat(
                    [remaining_df,updated_project_df],ignore_index=True)
                excel.save_data(final_df)
                st.success("Changes saved successfully.")
            except PermissionError:
                st.error("Please close the Excel file before saving.")
            except Exception as e:
                st.error(f"Unable to save data: {e}")
        
        #Calendar view
        st.markdown("---")
        st.subheader("Project Calendar")
        events = []  
        for _, row in filtered_df.iterrows():
            start_date = pd.to_datetime(row["Start_Date"],errors="coerce")
            end_date = pd.to_datetime(row["End_Date"],errors="coerce")
       
            if pd.isna(start_date) or pd.isna(end_date):
                continue
            #Calendar color scheme
            job_colors = {
                "Understanding Document": "#063888",
                "Design Document": "#0C411A",
                "Coding": "#E6CC7E",
                "Testing": "#51150F",
                "Audit": "#4D4949",
                "ITP": "#4A0D3D"
            }
     
            events.append({
                "title": f"{row['Employee_Name']} - {row['Job_Undertaken']}",
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "color": job_colors.get(row["Job_Undertaken"])
            })

        calendar(events=events,options={
           "initialView": "dayGridMonth",
           "headerToolbar": {
               "left": "prev,next today",
               "center": "title",
               "right": "dayGridMonth"
           },
           "editable": False,
           "selectable": False,
           "navLinks": True,
           "height": 700
       },
       key="project_calendar"
    )

show_job_list = JobListPage.show_job_list
 