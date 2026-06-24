import streamlit as st
import pandas as pd
import os
from styles import load_css
 
class EmployeeDetailsPage:
    #load method to read excel and show details
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
    <h2 style='margin:0;'>Employee Details</h2>
        </div>
                    """, unsafe_allow_html=True)
    
        #css script for styling
        st.markdown("""
<style>
.block-container { padding-top: 3rem; padding-bottom: 5rem; }
[data-testid="metric-container"] { background-color: #F5F7FA; border: 1px solid #DDE2E7; padding: 15px; border-radius: 10px; }
h3 { color: #1F3A5F; }
div[data-testid="stDataFrame"] { border: 1px solid #DDE2E7; border-radius: 10px; }
.stButton button { background-color: #1F3A5F; color: white; border-radius: 8px; border: none; }
.stButton button:hover { background-color: #2B4E7A; }
.my-details-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 20px; margin-bottom: 24px; }
.my-details-top { display: flex; gap: 20px; align-items: center; margin-bottom: 20px; flex-wrap: wrap; }
.my-details-avatar { width: 120px; height: 120px; border-radius: 18px; border: 2px solid #7c5cff; display: flex; align-items: center; justify-content: center; font-size: 50px; background: #ffffff; color: #7c5cff; }
.my-details-name { font-size: 24px; font-weight: 700; margin-bottom: 8px; color: #f8fbff; }
.my-details-meta { color: #c5d2ff; font-size: 14px; }
.details-table { width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.04); }
.details-table th, .details-table td { border: 1px solid rgba(124,92,255,0.16); padding: 12px 14px; text-align: left; }
.details-table th { background: rgba(124,92,255,0.12); color: #f8fbff; font-weight: 600; }
.details-table td { color: #eaf1ff; }
.details-table tr:hover { background: rgba(124,92,255,0.08); }
.directory-card { border: 1px solid #7c5cff; border-radius: 16px; background: rgba(124,92,255,0.08); padding: 18px; margin-bottom: 24px; }
.directory-table { width: 100%; border-collapse: collapse; margin-top: 16px; }
.directory-table th, .directory-table td { border: 1px solid rgba(124,92,255,0.16); padding: 12px 14px; text-align: left; }
.directory-table th { background: rgba(124,92,255,0.12); color: #f8fbff; font-weight: 700; }
.directory-table td { color: #eaf1ff; }
.directory-table tr:hover { background: rgba(124,92,255,0.08); }
</style>
""", unsafe_allow_html=True)
    
      
 
        # Read Excel
        try:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            FILE_PATH = os.path.join(BASE_DIR, "..", "employeedetails.xlsx")
            raw_df = pd.read_excel(FILE_PATH)
            raw_df.columns = raw_df.columns.str.strip().str.lower()
        except FileNotFoundError:
            st.error("Employee data file not found. Please make sure 'employeedetails.xlsx' exists.")
            return
        except Exception as e:
            st.error(f"Failed to load employee data: {e}")
            return
        #display metrics as cards and table for employee details
 
        st.markdown('### Workforce Overview')
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Employees", len(raw_df))
        c2.metric("Departments", raw_df["department"].nunique())
        c3.metric("Active Projects", (raw_df["status"].str.lower() == "active").sum())
        c4.metric("Inactive Projects", (raw_df["status"].str.lower() == "inactive").sum())
 
        df = pd.DataFrame()
        df["Employee ID"] = raw_df.iloc[:, 0].astype(str).str.strip()
        df["Name"] = raw_df.iloc[:, 1].astype(str).str.strip()
        df["Department"] = raw_df.iloc[:, 2].astype(str).str.strip()
        df["Designation"] = raw_df.iloc[:, 3].astype(str).str.strip()
        df["Status"] = raw_df.iloc[:, 4].astype(str).str.strip()
        df["Username"] = raw_df.iloc[:, 5].astype(str).str.strip()
        df["Role"] = raw_df.iloc[:, 6].astype(str).str.strip()
        df["DOB"] = raw_df.iloc[:, 7].astype(str).str.strip()
        df["Date of Joining"] = raw_df.iloc[:, 8].astype(str).str.strip()
        df["Email"] = raw_df.iloc[:, 9].astype(str).str.strip()
        df["Phone NO"] = raw_df.iloc[:, 10].astype(str).str.strip()
 
        username = st.session_state.get("Username", "").strip().lower()
        role = st.session_state.get("role", "")
 
        my_row = df[df["Username"].str.lower() == username]
 
        if not my_row.empty:
            me = my_row.iloc[0]
 
            st.markdown("## My Details")
            detail_html = f"""
<div class="my-details-card">
  <div class="my-details-top">
    <div class="my-details-avatar">👤</div>
    <div>
      <div class="my-details-name">{me['Name']}</div>
      <div class="my-details-meta"><strong>Role:</strong> {me['Role']} &nbsp; · &nbsp; <strong>Designation:</strong> {me['Designation']}</div>
    </div>
  </div>
  <table class="details-table">
    <thead>
      <tr><th>Field</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Employee ID</td><td>{me['Employee ID']}</td></tr>
      <tr><td>Department</td><td>{me['Department']}</td></tr>
      <tr><td>Status</td><td>{me['Status']}</td></tr>
      <tr><td>DOB</td><td>{me['DOB']}</td></tr>
      <tr><td>Date of Joining</td><td>{me['Date of Joining']}</td></tr>
      <tr><td>Email</td><td>{me['Email']}</td></tr>
      <tr><td>Phone NO</td><td>{me['Phone NO']}</td></tr>
    </tbody>
  </table>
</div>
"""
            st.markdown(detail_html, unsafe_allow_html=True)
        else:
            st.warning(f"No details found for username: {username}")

        role=st.session_state.get("role","").strip().lower()
        if role=="team member":
            return
        
 
        st.markdown("---")
        st.subheader("Employee Directory")
 
        # Filter section to filter employee details based on name, department and status and edit
        with st.expander("Filters", expanded=True):
            f1, f2, f3 = st.columns(3)
            with f1:
                search = st.text_input("Search by name or ID", placeholder="Type employee name or ID")
            with f2:
                dept = st.selectbox("Filter by Department", ["All"] + sorted(df["Department"].unique().tolist()))
            with f3:
                status = st.selectbox("Filter by Status", ["All"] + sorted(df["Status"].unique().tolist()))
 
        filtered_df = df.copy()
 
        if search:
            filtered_df = filtered_df[
                filtered_df["Name"].str.contains(search, case=False) |
                filtered_df["Employee ID"].str.contains(search, case=False)
            ]
        if dept != "All":
            filtered_df = filtered_df[filtered_df["Department"] == dept]
        if status != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status]
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        if filtered_df.empty:
            st.info("No employees found matching the criteria.")
            return
        
        #displaying the filtered dataframe with selected columns in a styled HTML table
        display_df = filtered_df[["Employee ID", "Name", "Department", "Designation", "Status", "DOB", "Date of Joining", "Email", "Phone NO"]].reset_index(drop=True)
        table_html = '<div class="directory-card"><h3>Employee Directory</h3>'
        table_html += '<table class="directory-table">'
        table_html += '<thead><tr>'
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
        
        #option to edit employee details for reporting manager role
       
 
        if role == "Reporting Manager":
            st.markdown("---")
            st.markdown("**Action**")
            selected_name = st.selectbox("Select employee to edit", [""] + filtered_df["Name"].tolist())
 
            if selected_name != "":
                selected = filtered_df[filtered_df["Name"] == selected_name].iloc[0]
 
                with st.expander(f"Edit - {selected_name}", expanded=True):
                    c1, c2 = st.columns(2)
                    new_name = c1.text_input("Employee Name", value=selected["Name"])
                    new_empid = c2.text_input("Emp ID", value=str(selected["Employee ID"]))
                    new_dept = c1.text_input("Department", value=selected["Department"])
                    new_desig = c2.text_input("Designation", value=selected["Designation"])
                    new_status = c1.selectbox("Status", ["Active", "Inactive"], index=0 if selected["Status"] == "Active" else 1)
 
                    col1, col2, _ = st.columns([1, 1, 4])
 
                    if col1.button("Save", use_container_width=True):
                        try:
                            full_df = pd.read_excel("employeedetails.xlsx")
                            full_df.columns = full_df.columns.str.strip().str.lower()
 
                            emp_id = str(selected["Employee ID"]).strip()
                            mask = full_df.iloc[:, 0].astype(str).str.strip() == emp_id
 
                            try:
                                full_df.loc[mask, full_df.columns[0]] = int(new_empid)
                            except ValueError:
                                full_df.loc[mask, full_df.columns[0]] = new_empid
 
                            full_df.loc[mask, full_df.columns[1]] = new_name
                            full_df.loc[mask, full_df.columns[2]] = new_dept
                            full_df.loc[mask, full_df.columns[3]] = new_desig
                            full_df.loc[mask, full_df.columns[4]] = new_status
 
                            full_df.to_excel("employeedetails.xlsx", index=False)
                            st.success(f"{selected_name} updated successfully!")
                            st.rerun()
                        except FileNotFoundError:
                            st.error("Could not save — file not found.")
                        except PermissionError:
                            st.error("Could not save — close the file in Excel and try again.")
                        except Exception as e:
                            st.error(f"Unexpected error while saving: {e}")
 
                    if col2.button("Back", use_container_width=True):
                        st.session_state.current_page = "Dashboard"
                        st.rerun()
 
 
def show_employee_details():
    EmployeeDetailsPage().show()