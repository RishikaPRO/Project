import streamlit as st
import pandas as pd
from styles import load_css
import plotly.express as px
 
 
class DashboardPage:
    #Load dashboard and get username and role
 
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
                    """, 
                    unsafe_allow_html=True)
    username = st.session_state.get("Username", "")
    role = st.session_state.get("role", "")
 
    employee_name = username
    reporting_manager = "Not Assigned"
    #read excel file
 
    try:
        emp_df = pd.read_excel("employeefinalu.xlsx")
        emp_df.columns = emp_df.columns.str.strip()
 
        user_row = emp_df[
            emp_df["username"].astype(str).str.lower()
            == username.lower()
        ]
 
        if not user_row.empty:
            employee_name = user_row.iloc[0]["name"]
    except Exception as e:
        st.error(f"Unable to load employee details: {e}")
        #css script for styling
 
    st.markdown(
        f"""
        <div style="
        background-color:#f8f9fa;
        padding:20px;
        border-radius:10px;
        margin-bottom:20px;
        ">
        <h2>Welcome, {employee_name}</h2>
        <h4>Role : {role}</h4>
 
        </div>
        """,
        unsafe_allow_html=True
    )
    #Header metrics for displaying
 
    col1, col2, col3 = st.columns(3)
 
    col1.metric("Projects", 15)
    col2.metric("Open Tasks", 8)
    col3.metric("Completed", 7)
 
    chart_data = {
        "Status": ["Open Tasks", "Completed"],
        "Count": [8, 7]
    }
    #Charts for displaying user Info
 
    chart_df = pd.DataFrame(chart_data)
 
    fig = px.pie(
        chart_df,
        values="Count",
        names="Status",
        title="Task Status Distribution",
        hole=0.4
    )
 
    st.plotly_chart(fig, use_container_width=True)
 
    st.divider()
 
    st.subheader("Quick Summary")
 
    st.info(
        f"""
        Employee : {employee_name}
 
        Role : {role}
        """
    )
 
 
def show_dashboard():
    DashboardPage().show_dashboard()
 