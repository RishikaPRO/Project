import streamlit as st
import pandas as pd
from datetime import datetime
from styles import load_css
 
class LeaveStatusPage:

    #Loading the excel file
    LEAVE_FILE = "leaveef.xlsx"
    ANNUAL_LEAVE = 24
 
    def load_data(self):
        try:
            df = pd.read_excel(self.LEAVE_FILE, sheet_name="Leave Tracker", header=None)
            records = []
            #Displaying Leave details and To display Leave Remaining
            for row in range(1,len(df)-1):
                emp_name = df.iloc[row, 0] 
                if pd.isna(emp_name):
                    continue
 
                emp_name = str(emp_name).strip()
 
                if not emp_name:
                    continue
 
                leave_this_month = pd.to_numeric(df.iloc[row,1], errors="coerce")
                leave_this_year = pd.to_numeric(df.iloc[row,2], errors="coerce")
 
                if pd.isna(leave_this_month):
                    leave_this_month = 0
 
                if pd.isna(leave_this_year):
                    leave_this_year = 0
 
                leave_remaining = self.ANNUAL_LEAVE - float(leave_this_year)
 
                records.append({
                    "Employee Name": emp_name,
                    "Leave This Month": leave_this_month,
                    "Leave This Year": leave_this_year,
                    "Leave Remaining": leave_remaining
                })
            return pd.DataFrame(records)
 
        except Exception as e:
            raise Exception(f"Unable to load leave data: {e}")
    #Displaying Total Leave metrics
 
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
    <h2 style='margin:0;'>Leave Status Dashboard</h2>
        </div>
                    """, unsafe_allow_html=True)
        try:
            df = self.load_data()
 
        except Exception as e:
            st.error(str(e))
            return
 
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Employees", len(df))
        c2.metric("Total Leave This Month", round(df["Leave This Month"].sum(), 1))
        c3.metric("Total Leave This Year", round(df["Leave This Year"].sum(), 1))
        c4.metric("Annual Leave Policy", "24")
        st.divider()
        search = st.text_input("Search Employee")
        if search:
            df = df[
                df["Employee Name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
 
def show_statusmail():
    LeaveStatusPage().show()
 
