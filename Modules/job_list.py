import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
import random
from styles import load_css
class JobListPage:
   FILE = "dashboard.xlsx"
   def detect_header_row(self, df):
       for i in range(min(30, len(df))):
           row = df.iloc[i].astype(str).str.lower()
           if row.str.contains("project id").any():
               return i
       return 0  
   def load_data(self):
       xl = pd.ExcelFile(self.FILE)
       all_data = []
       for sheet in xl.sheet_names:
           raw = pd.read_excel(self.FILE, sheet_name=sheet, header=None)
           raw = raw.dropna(how="all")
           header_row = None
           for i in range(min(20, len(raw))):
               row = raw.iloc[i].astype(str).str.lower()
               if "project id" in row.values or row.str.contains("project id").any():
                   header_row = i
                   break
           if header_row is None:
               continue
           df = pd.read_excel(
              self.FILE,                                                                                                                                                                                                                                                                                                                                        
              sheet_name=sheet,
              header=header_row
           )
           df.columns = df.columns.astype(str).str.strip()
           df = df.dropna(how="all")
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
                   "Release Date": r.get("Release Date", ""),
                   "_sheet_source": sheet # <-- CRITICAL: Track which sheet this project lives in
               })
       return pd.DataFrame(all_data)
   # FIXED: Safely updates specific rows across an existing multi-sheet workbook
   def save_update(self, overall_df):
       # 1. Read all original sheets as raw structures to preserve untouched tabs
       xl = pd.ExcelFile(self.FILE)
       sheets_dict = {}
       for sheet in xl.sheet_names:
           # We fetch using header=None to retain the complete exact structural shape of the original file
           sheets_dict[sheet] = pd.read_excel(self.FILE, sheet_name=sheet, header=None)
       # 2. Update the specific sheets that contain changes
       for sheet, sheet_grp in overall_df.groupby("_sheet_source"):
           # Fetch the original layout
           raw_sheet = sheets_dict[sheet]
           # Find where the headers start dynamically
           header_idx = self.detect_header_row(raw_sheet)
           # Drop tracking flag metadata column before exporting back
           clean_grp = sheet_grp.drop(columns=["_sheet_source"])
           # Extract header names from the clean group
           headers = clean_grp.columns.tolist()
           # Generate the update block: Headers row + Data rows
           update_df = pd.DataFrame([headers] + clean_grp.values.tolist())
           # Slice and stitch: retain anything above the header row, attach the updated block
           top_part = raw_sheet.iloc[:header_idx]
           sheets_dict[sheet] = pd.concat([top_part, update_df], ignore_index=True)
       # 3. Write back using ExcelWriter to preserve all sheets
       with pd.ExcelWriter(self.FILE, engine="openpyxl") as writer:
           for sheet_name, sheet_df in sheets_dict.items():
               sheet_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
   def color(self, pid):
       random.seed(str(pid))
       return "#{:06x}".format(random.randint(0, 0xFFFFFF))
   def show(self):
       load_css()
       st.markdown("""
<div style='padding:20px; border-radius:12px; background:linear-gradient(90deg,#0f172a,#1e293b); color:white; margin-bottom:20px;'>
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
                   
    /*Custom styling for your Streamlit buttons */
        div.stButton > button, div[data-testid="stForm"] button[type="submit"] {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 1px solid #7c5cff !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.3s ease !important;
        }
        /* Hover state style matching your photo */
        div.stButton > button:hover, div[data-testid="stForm"] button[type="submit"]:hover {
            background-color: #7c5cff !important;
            color: #ffffff !important;
            border-color: #9075ff !important;
            box-shadow: 0 0 10px rgba(124, 92, 255, 0.5) !important;
        }
</style>
       """, unsafe_allow_html=True)
       df = self.load_data()
       if df.empty:
           st.error("No usable data found")
           return
       df = df.fillna("")
       role = st.session_state.get("role", "")
       username = st.session_state.get("Username", "").strip()
       if role == "Team Member":
           member_df = df[df["Team Members"].astype(str).str.contains(username, case=False, na=False)]
           st.subheader("My Projects")
           if member_df.empty:
               st.info("No projects assigned to you")
               return
           for _, row in member_df.iterrows():
               status = str(row["Job Status"]).strip().lower()
               border = "#15532b" if status == "completed" else "#501e14" if status == "in progress" else "#1a3054"
               st.markdown(f"""
<div style="background:#1e293b; color:white; padding:20px; border-radius:12px; margin-bottom:15px; border-left:8px solid {border}; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
<h3>{row['Project Name']}</h3>
<p><b>Project ID:</b> {row['Project ID']}</p>
<p><b>Project Type:</b> {row['Project Type']}</p>
<p><b>Project Team:</b> {row['Project Team']}</p>
<p><b>Language:</b> {row['Language']}</p>
<p><b>Status:</b> {row['Job Status']}</p>
<p><b>Start Date:</b> {row['Start Date']}</p>
<p><b>Release Date:</b> {row['Release Date']}</p>
</div>
               """, unsafe_allow_html=True)
           st.divider()
           st.subheader("My Timeline")
           events = []
           for _, r in member_df.iterrows():
               start = pd.to_datetime(r["Start Date"], errors="coerce")
               end = pd.to_datetime(r["Release Date"], errors="coerce")
               if pd.isna(start): continue
               if pd.isna(end): end = start
               events.append({
                   "title": f"{r['Project ID']} - {r['Project Name']}",
                   "start": start.strftime("%Y-%m-%d"),
                   "end": end.strftime("%Y-%m-%d"),
                   "color": self.color(r["Project ID"])
               })
           calendar(events=events, options={"initialView": "dayGridMonth", "height": 700}, key="member_calendar")
       else:
           st.subheader("Project Table")
           # Filter out the operational metadata column so it doesn't render in the UI table
           display_df = df.drop(columns=["_sheet_source"], errors="ignore")
           table_html = '<div class="project-table-card"><h4>Project Table</h4><table class="project-table"><thead><tr>'
           for col in display_df.columns:
               table_html += f'<th>{col}</th>'
           table_html += '</tr></thead><tbody>'
           for _, row in display_df.iterrows():
               table_html += '<tr>'
               for value in row:
                   table_html += f'<td>{value}</td>'
               table_html += '</tr>'
           table_html += '</tbody></table></div>'
           st.markdown(table_html, unsafe_allow_html=True)
           st.divider()
           st.subheader("Edit Project")
           project_ids = df["Project ID"].dropna().unique().tolist()
           selected_id = st.selectbox("Select Project ID", project_ids)
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
               if save:
                   df.loc[df["Project ID"] == selected_id, "Project Name"] = new_name
                   df.loc[df["Project ID"] == selected_id, "Project Type"] = new_type
                   df.loc[df["Project ID"] == selected_id, "Team Members"] = new_team
                   df.loc[df["Project ID"] == selected_id, "Job Status"] = new_status
                   df.loc[df["Project ID"] == selected_id, "Start Date"] = new_start
                   df.loc[df["Project ID"] == selected_id, "Release Date"] = new_end
                   self.save_update(df)
                   st.success("Updated Successfully")
                   st.rerun()
               if st.button("Delete Record", key=f"delete_{selected_id}"):
                   df = df[df["Project ID"] != selected_id]
                   self.save_update(df)
                   st.success("Record Deleted")
                   st.rerun()
               st.divider()
               st.subheader("Timeline")
               events = []
               for _, r in df.iterrows():
                   start = pd.to_datetime(r["Start Date"], errors="coerce")
                   end = pd.to_datetime(r["Release Date"], errors="coerce")
                   if pd.isna(start): continue
                   if pd.isna(end): end = start
                   events.append({
                       "title": f"{r['Project ID']} - {r['Project Name']}",
                       "start": start.strftime("%Y-%m-%d"),
                       "end": end.strftime("%Y-%m-%d"),
                       "color": self.color(r["Project ID"])
                   })
               calendar(events=events, options={"initialView": "dayGridMonth", "height": 700}, key="calendar")
def show_job_list():
   JobListPage().show()