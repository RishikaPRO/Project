import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import random
from styles import load_css

class JobListPage:
    FILE = "dashboard.xlsx"

    #Auto header detection from excel file
    def detect_header_row(self, df):
        """
        Finds row containing 'Project ID' or similar keyword
        """
        for i in range(min(30, len(df))):
            row = df.iloc[i].astype(str).str.lower()
            if row.str.contains("project id").any():
                return i
        return 0  
    
    #load data from excel file
    def load_data(self):
        xl = pd.ExcelFile(self.FILE)
        all_data = []
        for sheet in xl.sheet_names:
            raw = pd.read_excel(self.FILE, sheet_name=sheet, header=None)
            raw = raw.dropna(how="all")
            
            #Find the header row
            header_row = None
            for i in range(min(20, len(raw))):
                row = raw.iloc[i].astype(str).str.lower()
                if "project id" in row.values or row.str.contains("project id").any():
                    header_row = i
                    break
                if header_row is None:
                    continue

            #Read table data
            df = pd.read_excel(
               self.FILE,
               sheet_name=sheet,
               header=header_row
            )
            df.columns = df.columns.astype(str).str.strip()
            #Remove empty rows
            df = df.dropna(how="all")
            
            
            #Normalize excel data
            def col(name):
                return df[name] if name in df.columns else ""
            for _, r in df.iterrows():
                pid = r.get("Project ID", "")
                if pd.isna(pid) or str(pid).strip() == "":
                    continue
                pid = str(pid).strip()
                if pid.lower() in ["nan", "none", "leads", "project id"]:
                    continue
                all_data.append({
                    "Project ID": pid,
                    "Project Name": r.get("Project Name", ""),
                    "Project Type": r.get("Project Type", ""),
                    "Project Team": r.get("Project Team", ""),
                    "Team Members": r.get("Team Members", ""),
                    "Language": r.get("Language", ""),
                    "Job Status": r.get("Job Status", ""),
                    "Start Date": r.get("Start Date", ""),
                    "Release Date": r.get("Release Date", "")
                })
        return pd.DataFrame(all_data)
    
    # Save data
    def save_update(self, df):
        df.to_excel(self.FILE, index=False)

    def color(self, pid):
        random.seed(str(pid))
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
    # job_list dashboard ui
    def show(self):
        load_css()
        st.markdown("""
        <div style='
        padding:20px;
            border-radius:12px;
            background:linear-gradient(90deg,#0f172a,#1e293b);
            color:white;
            margin-bottom:20px;
        '>
    <h2 style='margin:0;'>Job List Dashboard </h2>
        </div>
                    """, unsafe_allow_html=True)
        
        df = self.load_data()
        if df.empty:
            st.error("No usable data found")
            return
        df = df.fillna("")

        role = st.session_state.get("role", "")
        username = st.session_state.get("username", "").strip()
        
        #
        if role == "Team Member":
            member_df = df[df["Team Members"].astype(str).str.contains(username, case=False, na=False)]
            st.subheader("My Projects")
            if member_df.empty:
                st.info("No projects assigned to you")
                return
            for _, row in member_df.iterrows():
                status = str(row["Job Status"]).strip().lower()
                if status == "completed":
                    border = "#15532b"
                elif status == "in progress":
                    border = "#501e14"
                else:
                    border = "#1a3054"
                st.markdown(
                    f"""
<div style="
               background:white;
               padding:20px;
               border-radius:12px;
               margin-bottom:15px;
               border-left:8px solid {border};
               box-shadow:0 2px 8px rgba(0,0,0,0.1);
           ">
<h3>{row['Project Name']}</h3>
<p><b>Project ID:</b> {row['Project ID']}</p>
<p><b>Project Type:</b> {row['Project Type']}</p>
<p><b>Project Team:</b> {row['Project Team']}</p>
<p><b>Language:</b> {row['Language']}</p>
<p><b>Status:</b> {row['Job Status']}</p>
<p><b>Start Date:</b> {row['Start Date']}</p>
<p><b>Release Date:</b> {row['Release Date']}</p>
</div>
           """,
                    unsafe_allow_html=True
                )
        
        #reporting manager view
        else:
            st.subheader("Project Table")
            st.dataframe(df, use_container_width=True)
            st.divider()
            st.subheader("Edit Project")
            project_ids = df["Project ID"].dropna().unique().tolist()
            selected_id = st.selectbox(
                "Select Project ID",
                project_ids
            )
            filtered = df[df["Project ID"] == selected_id]
            if not filtered.empty:
                selected_row = filtered.iloc[0]
                with st.form("edit_form"):
                    new_name = st.text_input(
                        "Project Name",
                        selected_row["Project Name"]
                    )
                    new_type = st.text_input(
                        "Project Type",
                        selected_row["Project Type"]
                    )
                    new_team = st.text_input(
                        "Team Members",
                        selected_row["Team Members"]
                    )
                    new_status = st.text_input(
                        "Job Status",
                        selected_row["Job Status"]
                    )
                    new_start = st.text_input(
                        "Start Date",
                        selected_row["Start Date"]
                    )
                    new_end = st.text_input(
                        "Release Date",
                        selected_row["Release Date"]
                    )
                    save = st.form_submit_button(
                        "Save Changes"
                    )
                if save:
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Project Name"
                    ] = new_name
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Project Type"
                    ] = new_type
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Team Members"
                    ] = new_team
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Job Status"
                    ] = new_status
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Start Date"
                    ] = new_start
                    df.loc[
                        df["Project ID"] == selected_id,
                        "Release Date"
                    ] = new_end
                    self.save_update(df)
                    st.success("Updated Successfully")
                    st.rerun()
                if st.button(
                    "Delete Record",
                    key=f"delete_{selected_id}"
                ):
                    df = df[df["Project ID"] != selected_id]
                    self.save_update(df)
                    st.success("Record Deleted")
                    st.rerun()
                
                # Calender view of the job timeline
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
 
 
