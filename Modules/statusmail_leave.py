import streamlit as st
import pandas as pd
from datetime import datetime
<<<<<<< HEAD
from styles import load_css
 
class LeaveStatusPage:
 
    LEAVE_FILE = "leaveef.xlsx"
    ANNUAL_LEAVE = 24
 
    def load_data(self):
        try:
            df = pd.read_excel(self.LEAVE_FILE, sheet_name="Leave Tracker", header=None)
            
            records = []
 
            # Employee rows start around row 8 in your file
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
 
 
    def show(self):
 
        load_css()
 
        st.title("Leave Status Dashboard")
 
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
 
=======
# ---------------- CONFIG ----------------
EXCEL_FILE = "reporting_manager_dashboard.xlsx"
TOTAL_LEAVE = 24
DEDUCTIBLE = {"P", "UP", "C", "ML", "PL", "Co", "H1", "H2"}

#excel document loading process
class ExcelManager:
   def __init__(self, file_path):
       self.file_path = file_path
   def load_data(self, sheet_name):
       return pd.read_excel(
           self.file_path,
           sheet_name=sheet_name,
           engine="openpyxl"
       )

#status mail summary
class StatusMailProcessor:
   @staticmethod
   def process(df):
       df = df.copy()
       df["MailSent"] = df["MailSent"].fillna("No")
       summary = df.groupby("Employee").agg(
           Total=("MailSent", "count"),
           Sent=("MailSent", lambda x: (x.str.lower() == "yes").sum()),
           Last_Sent_Date=("Date", "max")
       ).reset_index()
       summary["Pending"] = summary["Total"] - summary["Sent"]
       summary["Completion %"] = (summary["Sent"] / summary["Total"]) * 100
       return df, summary

#leave summary
class LeaveProcessor:
   @staticmethod
   def compute(df):
       df = df.copy()
       def calc(x):
           if x in ["H1", "H2"]:
               return 0.5
           if x in DEDUCTIBLE:
               return 1
           return 0
       df["LeaveValue"] = df["LeaveType"].apply(calc)
      
       # Total leave
       total = df.groupby("Employee")["LeaveValue"].sum().reset_index()
       total.rename(columns={"LeaveValue": "Total_Leave_Taken"}, inplace=True)
       total["Leave_Remaining"] = TOTAL_LEAVE - total["Total_Leave_Taken"]
      
       # Monthly leave
       now = datetime.now()
       monthly = df[
           (df["Date"].dt.month == now.month) &
           (df["Date"].dt.year == now.year)
       ].groupby("Employee")["LeaveValue"].sum().reset_index()
       monthly.rename(columns={"LeaveValue": "Monthly_Leave"}, inplace=True)
       # Yearly leave
       yearly = df[df["Date"].dt.year == now.year] \
           .groupby("Employee")["LeaveValue"].sum().reset_index()
       yearly.rename(columns={"LeaveValue": "Yearly_Leave"}, inplace=True)
       
       #overall leave calculations
       final = total.merge(monthly, on="Employee", how="left") \
                    .merge(yearly, on="Employee", how="left") \
                    .fillna(0)
       return df, final

#dashboard upon opening
class ReportingManagerDashboard:
   @classmethod
   def show_statusmail(cls):
       st.title("Status Mail Dashboard")
       excel = ExcelManager(EXCEL_FILE)
       try:
           status_df = excel.load_data("status_mail")
           status_df["Date"] = pd.to_datetime(status_df["Date"])
       except Exception as e:
           st.error(f"Error loading status mail data: {e}")
           st.stop()
       raw, summary = StatusMailProcessor.process(status_df)
       st.subheader("Summary")
       st.dataframe(summary)
       st.bar_chart(summary.set_index("Employee")[["Sent", "Pending"]])

   @classmethod
   def show_leave_records(cls):
       st.title("Leave Records Dashboard (Reporting Manager)")
       excel = ExcelManager(EXCEL_FILE)
       try:
           leave_df = excel.load_data("leave_records")
           leave_df["Date"] = pd.to_datetime(leave_df["Date"])
       except Exception as e:
           st.error(f"Error loading leave data: {e}")
           st.stop()
       raw, summary = LeaveProcessor.compute(leave_df)
       st.subheader("Leave Summary")
       st.dataframe(summary)
       st.bar_chart(
           summary.set_index("Employee")[[
               "Total_Leave_Taken",
               "Monthly_Leave",
               "Yearly_Leave",
               "Leave_Remaining"
           ]]
       )

#function exports
def show_statusmail():
   ReportingManagerDashboard.show_statusmail()

def show_leave_records():
   ReportingManagerDashboard.show_leave_records()
>>>>>>> bf1327778f1af11554c5d05d965d974ef814b5c4
