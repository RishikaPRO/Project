import streamlit as st
import pandas as pd
 
def show_employee_details():
    
    st.title("Employee Details")
    st.markdown("""
<style>
 
/* Main page spacing */
.block-container {
    padding-top: 3rem;
    padding-bottom:4rem;
}
 
/* Metric cards */
[data-testid="metric-container"] {
    background-color: #F5F7FA;
    border: 1px solid #DDE2E7;
    padding: 15px;
    border-radius: 10px;
}
 
/* Section headings */
h3 {
    color: #1F3A5F;
}
 
/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #DDE2E7;
    border-radius: 10px;
}
 
/* Buttons */
.stButton button {
    background-color: #1F3A5F;
    color: white;
    border-radius: 8px;
    border: none;
}
 
.stButton button:hover {
    background-color: #2B4E7A;
}
 
</style>
""", unsafe_allow_html=True)
    st.caption("View and manage employee information")
 
    # Read Excel
    raw_df = pd.read_excel("employeefinal.xlsx")
    raw_df.columns = raw_df.columns.str.strip().str.lower()
    st.markdown('### Workforce Overview')
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Employees", len(raw_df))
    c2.metric("Departments", raw_df["department"].nunique())
    c3.metric("Active", (raw_df["status"].str.lower() == "active").sum())
    c4.metric("Inactive", (raw_df["status"].str.lower() == "inactive").sum())
 
    df = pd.DataFrame()
    df["Employee ID"] = raw_df.iloc[:, 0].astype(str).str.strip()
    df["Name"]        = raw_df.iloc[:, 1].astype(str).str.strip()
    df["Department"]  = raw_df.iloc[:, 2].astype(str).str.strip()
    df["Designation"] = raw_df.iloc[:, 3].astype(str).str.strip()
    df["Status"]      = raw_df.iloc[:, 4].astype(str).str.strip()
    df["Role"]        = raw_df.iloc[:, 6].astype(str).str.strip()
    df["Username"]    = raw_df.iloc[:, 5].astype(str).str.strip()
 
    username = st.session_state.get("Username", "").strip().lower()
    role = st.session_state.get("role", "")
 
  
    my_row = df[df["Username"].str.lower() == username]

 
    with st.container(border=True):
        st.subheader("My Details")
    if not my_row.empty:
        me = my_row.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Name",        me["Name"])
        c2.metric("Employee ID", me["Employee ID"])
        c3.metric("Department",  me["Department"])
        c4.metric("Designation", me["Designation"])
    else:
        st.warning(f"No details found for username: **{username}** — check your Excel username column.")
    
    st.markdown("---")
    st.subheader("Employee Directory")
 
    # ── Filters ──
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
 
   
    display_df = filtered_df[["Employee ID", "Name", "Department", "Designation", "Status"]].reset_index(drop=True)

    st.dataframe(display_df, use_container_width=True, hide_index=True)
 

    if role == "Reporting Manager":
        st.markdown("---")
        st.markdown("**Action**")
        selected_name = st.selectbox("Select employee to edit", [""] + filtered_df["Name"].tolist())
 
        if selected_name != "":
            selected = filtered_df[filtered_df["Name"] == selected_name].iloc[0]
 
            with st.expander(f"Edit - {selected_name}", expanded=True):
                c1, c2 = st.columns(2)
                new_name   = c1.text_input("Employee Name", value=selected["Name"])
                new_empid  = c2.text_input("Emp ID",        value=str(selected["Employee ID"]))
                new_dept   = c1.text_input("Department",    value=selected["Department"])
                new_desig  = c2.text_input("Designation",   value=selected["Designation"])
                new_status = c1.selectbox(
                    "Status", ["Active", "Inactive"],
                    index=0 if selected["Status"] == "Active" else 1
                )
 
                col1, col2, _ = st.columns([1, 1, 4])
 
                if col1.button("Save", use_container_width=True):
                    full_df = pd.read_excel("employeefinal.xlsx")
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
 
                    full_df.to_excel("employeefinal.xlsx", index=False)
                    st.success(f"{selected_name} updated successfully!")
                    st.rerun()
 
                if col2.button("Back", use_container_width=True):
                    st.session_state.current_page = "Dashboard"
                    st.rerun()