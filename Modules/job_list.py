import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import random
class JobListPage:
    FILE = "AD_Weekly_Load_Tracking_2026-27.xlsx"
    # ---------------- LOAD ----------------
    def load_data(self):
        xl = pd.ExcelFile(self.FILE)
        records = []
        for sheet in xl.sheet_names:
            df = pd.read_excel(self.FILE, sheet_name=sheet, header=None)
            for i in range(4, 17):
                row = df.iloc[i]
                if row.isnull().all():
                    continue
                project_id = row[2]
                if pd.isna(project_id):
                    continue
                project_id = str(project_id).strip()
                if project_id.lower() in ["leads", "project id", "nan"]:
                    continue
                def safe(idx):
                    return row[idx] if len(row) > idx else None
                records.append({
                    "Project ID": project_id,
                    "Project Name": safe(3),
                    "Project Type": safe(4),
                    "Project Team": safe(10),
                    "Team Members": safe(6),
                    "Language": safe(14),
                    "Job Status": safe(16),
                    "Start Date": safe(11),
                    "Release Date": safe(12)
                })
        return pd.DataFrame(records)
    # ---------------- SAVE ----------------
    def save_update(self, df):
        df.to_excel(self.FILE, index=False)
    # ---------------- COLOR ----------------
    def color(self, pid):
        random.seed(str(pid))
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    # ---------------- UI ----------------
    def show(self):
        st.title(" Job List Dashboard")
        df = self.load_data()
        df=df.fillna("")
        for col in df.columns:
            df[col]=df[col].astype("object")
        if df.empty:
            st.error("No usable data found")
            return
 
        # ---------------- EDIT BUTTON (BOTTOM) ----------------
        st.subheader("Project Table")
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.subheader("Edit Project")
        project_ids = df["Project ID"].dropna().unique().tolist()
        selected_id = st.selectbox("Select Project ID", project_ids)
        selected_row = df[df["Project ID"] == selected_id].iloc[0]
        with st.form("edit_form"):
            new_name = st.text_input("Project Name", selected_row["Project Name"])
            new_type = st.text_input("Project Type", selected_row["Project Type"])
            new_team = st.text_input("Team Members", selected_row["Team Members"])
            new_status = st.text_input("Job Status", selected_row["Job Status"])
            new_start =  st.text_input("Start Date", selected_row["Start Date"])
            new_end = st.text_input("Release Date", selected_row["Release Date"])
            save = st.form_submit_button("Save Changes")
        if save:
            df.loc[df["Project ID"] == selected_id, "Project Name"] = new_name
            df.loc[df["Project ID"] == selected_id, "Project Type"] = new_type
            df.loc[df["Project ID"] == selected_id, "Team Members"] = new_team
            df.loc[df["Project ID"] == selected_id, "Job Status"] = new_status
            df.loc[df["Project ID"] == selected_id, "Start Date"] = new_start
            df.loc[df["Project ID"] == selected_id, "Release Date"] = new_end
            df.to_excel(self.FILE, index=False)
            st.success(" Updated successfully")
            st.rerun()
        # ---------------- CALENDAR ----------------
        st.divider()
        st.subheader("Timeline")
        events = []
        for _, r in df.iterrows():
            start = pd.to_datetime(r["Start Date"], errors="coerce")
            end = pd.to_datetime(r["Release Date"], errors="coerce")
            if pd.isna(start):
                continue
            if pd.isna(end):
                end = start
            events.append({
                "title": f"{r['Project ID']} - {r['Project Name']}",
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
                "color": self.color(r["Project ID"])
            })
        calendar(
            events=events,
            options={
                "initialView": "dayGridMonth",
                "headerToolbar": {
                    "left": "prev,next today",
                    "center": "title",
                    "right": "dayGridMonth,timeGridWeek"
                },
                "height": 700
            },
            key="calendar"
        )
 
def show_job_list():
    JobListPage().show()
 
 