import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import random
from styles import load_css

class JobListPage:
    FILE = "dashboard.xlsx"

    #Auto header detection from excel file
    def detect_header_row(self, df):
        #Find Project_ID                               
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
        <style>
        .project-table-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 14px; margin-bottom: 24px; max-width: 100%; overflow-x: auto; }
        .project-table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }
        .project-table th, .project-table td { border: 1px solid rgba(124,92,255,0.16); padding: 8px 10px; text-align: left; }
        .project-table th { background: rgba(124,92,255,0.12); color: #f8fbff; font-weight: 700; }
        .project-table td { color: #eaf1ff; }
        .project-table tr:hover { background: rgba(124,92,255,0.08); }
        .project-table h4 { margin: 0 0 8px; color: #f8fbff; font-size: 16px; }
        </style>
                    """, unsafe_allow_html=True)
        
        df = self.load_data()
        if df.empty:
            st.error("No usable data found")
            return
        df = df.fillna("")

        role = st.session_state.get("role", "")
        username = st.session_state.get("Username", "").strip()
        
        #Team member view
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
    background:#1e293b;
    color:white;
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

            st.divider()
            st.subheader("My Timeline")
            events = []
            for _, r in member_df.iterrows():
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
            calendar(events=events,
                options={
                    "initialView": "dayGridMonth",
                    "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek"},
                    "height": 700
                },
                key="member_calendar")
        
        #reporting manager view
        else:
            st.subheader("Project Table")
            table_html = '<div class="project-table-card">'
            table_html += '<h4>Project Table</h4>'
            table_html += '<table class="project-table">'
            table_html += '<thead><tr>'
            for col in df.columns:
                table_html += f'<th>{col}</th>'
            table_html += '</tr></thead><tbody>'
            for _, row in df.iterrows():
                table_html += '<tr>'
                for value in row:
                    table_html += f'<td>{value}</td>'
                table_html += '</tr>'
            table_html += '</tbody></table></div>'
            st.markdown(table_html, unsafe_allow_html=True)
            st.divider()
            st.subheader("Edit Project")
            project_ids = df["Project ID"].dropna().unique().tolist()
            selected_id = st.selectbox("Select Project ID",project_ids)
            filtered = df[df["Project ID"] == selected_id]
            if not filtered.empty:
                selected_row = filtered.iloc[0]
                with st.form("edit_form"):
                    new_name = st.text_input("Project Name", selected_row["Project Name"])
                    new_type = st.text_input("Project Type", selected_row["Project Type"])
                    new_team = st.text_input("Team Members", selected_row["Team Members"])
                    new_status = st.text_input("Job Status", selected_row["Job Status"])
                    new_start = st.text_input("Start Date", selected_row["Start Date"])
                    new_end = st.text_input("Release Date", selected_row["Release Date"])
                    save = st.form_submit_button("Save Changes")
               
                #Edited data updation          
                if save:
                    df.loc[df["Project ID"] == selected_id, "Project Name"] = new_name
                    df.loc[df["Project ID"] == selected_id,"Project Type"] = new_type
                    df.loc[df["Project ID"] == selected_id,"Team Members"] = new_team
                    df.loc[df["Project ID"] == selected_id,"Job Status"] = new_status
                    df.loc[df["Project ID"] == selected_id,"Start Date"] = new_start
                    df.loc[ df["Project ID"] == selected_id, "Release Date"] = new_end
                    self.save_update(df)
                    st.success("Updated Successfully")
                    st.rerun()
                if st.button("Delete Record", key=f"delete_{selected_id}"):
                    df = df[df["Project ID"] != selected_id]
                    self.save_update(df)
                    st.success("Record Deleted")
                    st.rerun()
                
                # Calendar view of the job timeline
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
